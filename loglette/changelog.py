import inspect
from collections import OrderedDict
from datetime import datetime
from enum import Enum
from functools import partial
from operator import itemgetter
from typing import Any, Dict, Iterable, Iterator, List, Optional, Reversible, TYPE_CHECKING, Tuple, Type, Union, overload

from .parser import Parser, ParserPType, get_parser, guess_parser
from .version import Version, VersionCompType

if TYPE_CHECKING:
    from .formatter import Formatter

_DEFAULT = object()


def find_parser(parser: Optional[ParserPType], text: str = None) -> Parser:
    if parser:
        parser = get_parser(parser)

    if not parser:
        if isinstance(text, str):
            parser = guess_parser(text)
        else:
            parser = get_parser("loglette")

    return parser


class ReleaseDate(Enum):
    UNRELEASED = "unreleased"
    NEVER = "never"

    def __str__(self) -> str:
        return self.value


HeaderPType = Union[str, Dict[str, str]]


class ChangelogHeader:
    version: Version
    release_date: Union[datetime, ReleaseDate]

    def __init__(self, version: Version, release_date: datetime):
        self.version = version
        self.release_date = release_date

    def __repr__(self) -> str:
        return f"version: {self.version};\nrelease: {self.release_date};"

    @classmethod
    def parse(cls, headers: HeaderPType, parser: ParserPType = None) -> "ChangelogHeader":
        if isinstance(headers, str):
            parser = find_parser(parser, headers)
            headers = parser.parse_header(headers)

        version = Version.parse(headers.pop("version"))
        release_date = headers.pop("release_date", None)
        if release_date:
            try:
                release_date = ReleaseDate(release_date)
            except ValueError:
                parser = find_parser(parser)
                release_date = parser.parse_date(release_date)
        else:
            release_date = ReleaseDate.UNRELEASED

        return cls(version, release_date)


ChangePType = Dict[str, str]
ChangesPType = Union[str, List[ChangePType]]


class Change:
    change_type: str
    priority: int
    text: str

    def __init__(self, change_type: str, priority: int, text: str):
        self.change_type = change_type
        self.priority = priority
        self.text = text

    def __repr__(self) -> str:
        return f"{self.change_type}[{self.priority}]: {self.text};"

    @classmethod
    def parse(cls, change: ChangePType, parser: ParserPType = None) -> "Change":
        if isinstance(change, str):
            parser = find_parser(parser, change)
            change = next(iter(parser.parse_changes(change)))

        change_type = change.pop("type")
        priority = change.pop("priority")
        if priority:
            priority = int(priority)
        else:
            priority = 0

        text = change.pop("text")

        return cls(change_type, priority, text)

    @classmethod
    def parse_changes(cls, changes: ChangesPType, parser: ParserPType = None) -> List["Change"]:
        if isinstance(changes, str):
            parser = find_parser(parser, changes)
            changes = parser.parse_changes(changes)

        _changes = []
        for change in changes:
            _change = cls.parse(change, parser=parser)
            _changes.append(_change)

        return _changes


ChangelogPType = Union[str, Tuple[HeaderPType, ChangesPType]]
FormatterType = Union[str, Type["Formatter"], "Formatter"]


class Changelog:
    header: ChangelogHeader
    changes: List[Change]

    def __init__(self, header: ChangelogHeader, changes: List[Change]):
        self.header = header
        self.changes = changes

    def __repr__(self) -> str:
        return f"Changelog v{self.version} ({len(self)} change(s))"

    def __len__(self) -> int:
        return len(self.changes)

    def __getattr__(self, item):
        return getattr(self.header, item)

    @classmethod
    def parse(cls, changelog: ChangelogPType, parser: ParserPType = None) -> "Changelog":
        if isinstance(changelog, str):
            parser = find_parser(parser, changelog)
            changelog = parser.split_changelog(changelog)

        header = ChangelogHeader.parse(changelog[0], parser=parser)
        changes = Change.parse_changes(changelog[1], parser=parser)
        return cls(header, changes)

    def loglette(self) -> str:
        changes = "\n".join(map(str, self.changes))
        return f"{self.header}\n---\n{changes}"

    def format(self, formatter: FormatterType, **options) -> Any:
        from .formatter import Formatter

        if isinstance(formatter, str):
            from .formatter import get_formatter
            formatter = get_formatter(formatter)

        if inspect.isclass(formatter) and issubclass(formatter, Formatter):
            formatter = formatter()

        if isinstance(formatter, Formatter):
            return formatter.format(self, **options)
        else:
            raise TypeError(f"Can't use {formatter} to format {self}")


ChangelogRangePType = Union[str, List[ChangelogPType]]

class ChangelogRange:
    _versions: OrderedDict
    _file_order: OrderedDict
    versions: Reversible[Version]
    changelogs: Reversible[Changelog]

    @overload
    def __init__(self, versions: Iterable[Changelog]):
        ...

    @overload
    def __init__(self, versions: Dict[Version, Changelog]):
        ...

    def __init__(self, versions):
        if isinstance(versions, list):
            _versions = [(changelog.version, changelog) for changelog in versions]
        else:
            _versions = list(versions.items())

        self._file_order = OrderedDict(_versions)
        self._versions = OrderedDict(sorted(_versions, key=itemgetter(0)))
        self.versions = self._versions.keys()
        self.changelogs = self._versions.values()

    def __str__(self) -> str:
        return f"{self.oldest} -> {self.latest}"

    def __len__(self) -> int:
        return len(self._versions)

    def __iter__(self) -> Iterator[Changelog]:
        return iter(self.changelogs)

    def __reversed__(self) -> Iterator[Changelog]:
        return reversed(self.changelogs)

    @overload
    def __getitem__(self, item: VersionCompType) -> Changelog:
        ...

    @overload
    def __getitem__(self, item: slice) -> "ChangelogRange":
        ...

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self._get_range(item.start, item.stop)
        return self.get(item)

    def __delitem__(self, key: VersionCompType):
        del self._versions[key]

    def __contains__(self, item: VersionCompType) -> bool:
        return item in self.versions

    @classmethod
    def parse(cls, changelogs: ChangelogRangePType, parser: ParserPType = None) -> "ChangelogRange":
        if isinstance(changelogs, str):
            parser = find_parser(parser, changelogs)
            changelogs = parser.split_changelogs(changelogs)

        changelogs = list(map(partial(Changelog.parse, parser=parser), changelogs))
        return cls(changelogs)

    @property
    def first(self) -> Optional[Changelog]:
        return next(iter(self._file_order.values()), None)

    @property
    def last(self) -> Optional[Changelog]:
        return next(reversed(self._file_order.values()), None)

    @property
    def oldest(self) -> Optional[Changelog]:
        return next(iter(self), None)

    @property
    def latest(self) -> Optional[Changelog]:
        return next(reversed(self.changelogs), None)

    def copy(self) -> "ChangelogRange":
        versions = self._versions.copy()
        inst = object.__new__(type(self))
        inst._versions = versions
        inst.versions = versions.keys()
        inst.changelogs = versions.values()
        return inst

    @overload
    def get(self, version: VersionCompType) -> Changelog:
        ...

    def get(self, version: VersionCompType, default: Any = _DEFAULT) -> Changelog:
        try:
            return self._versions.get(version)
        except KeyError:
            if default is _DEFAULT:
                raise
            return default

    def _get_range(self, start: Optional[VersionCompType], stop: Optional[VersionCompType]) -> "ChangelogRange":
        version_range = self.copy()

        if start:
            for version in self.versions:
                if version < start:
                    del version_range[version]
                else:
                    break

        if stop:
            for version in reversed(self.versions):
                if version >= stop:
                    del version_range[version]
                else:
                    break

        return version_range

    def flatten(self) -> Changelog:
        changes = []
        for changelog in reversed(self):
            changes.extend(changelog.changes)
        last = self.latest
        header = ChangelogHeader(last.version, last.release_date)
        return Changelog(header, changes)
