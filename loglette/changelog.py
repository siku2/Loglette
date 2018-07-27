from datetime import datetime
from typing import Any, Dict, List, TYPE_CHECKING, Tuple, Type, Union

from . import parser
from .version import Version

if TYPE_CHECKING:
    from .formatter import Formatter

HeaderPType = Union[str, Dict[str, str]]


class ChangelogHeader:
    version: Version
    release_date: datetime

    def __init__(self, version: Version, release_date: datetime):
        self.version = version
        self.release_date = release_date

    def __repr__(self) -> str:
        return f"version: {self.version};\nrelease: {self.release_date};"

    @classmethod
    def parse(cls, headers: HeaderPType) -> "ChangelogHeader":
        if isinstance(headers, str):
            headers = parser.parse_header(headers)

        version = Version.parse(headers.pop("version"))
        release_date = headers.pop("release", None)
        if release_date:
            release_date = parser.parse_date(release_date)

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
        return f"{self.change_type}[{self.priority}]: \"{self.text}\";"

    @classmethod
    def parse(cls, change: ChangePType) -> "Change":
        change_type = change.pop("type")
        priority = change.pop("priority", 0)
        if priority:
            priority = int(priority)

        text = change.pop("text")

        return cls(change_type, priority, text)

    @classmethod
    def parse_changes(cls, changes: ChangesPType) -> List["Change"]:
        if isinstance(changes, str):
            changes = parser.parse_changes(changes)

        _changes = []
        for change in changes:
            _change = cls.parse(change)
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

    def __getattr__(self, item):
        return getattr(self.header, item)

    @classmethod
    def parse(cls, changelog: ChangelogPType) -> "Changelog":
        if isinstance(changelog, str):
            changelog = parser.split_changelog(changelog)

        header = ChangelogHeader.parse(changelog[0])
        changes = Change.parse_changes(changelog[1])
        return cls(header, changes)

    def loglette(self) -> str:
        changes = "\n".join(map(str, self.changes))
        return f"{self.header}\n---\n{changes}"

    def format(self, formatter: FormatterType, **options) -> Any:
        from .formatter import Formatter

        if isinstance(formatter, str):
            from .formatter import get_formatter
            formatter = get_formatter(formatter)

        if issubclass(formatter, Formatter):
            formatter = formatter()

        if isinstance(formatter, Formatter):
            return formatter.format(self, **options)
        else:
            raise TypeError(f"Can't use {formatter} to format {self}")
