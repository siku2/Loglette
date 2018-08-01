import abc
import inspect
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Iterable, Mapping, Tuple, Type, Union

from dateutil.parser import parser as DateParser

from ..utils import import_directory

_ALIAS_MAP = {}
_PARSERS = set()


class Parser(abc.ABC):
    def __init__(self):
        self.date_parser = DateParser()

    def parse_date(self, value: str) -> datetime:
        return self.date_parser.parse(value)

    def can_handle(self, text: str) -> bool:
        """Check whether this parser can parse the text"""
        try:
            changelogs = self.split_changelogs(text)
            if not changelogs:
                return False
            for changelog in changelogs:
                _header, _changes = self.split_changelog(changelog)
                if not any((_header, _changes)):
                    return False
                header = self.parse_header(_header)
                changes = self.parse_changes(_changes)

                if not any((header, changes)):
                    return False
        except Exception:
            return False
        else:
            return True

    @abc.abstractmethod
    def parse_header(self, text: str) -> Mapping[str, str]:
        """Parse the header of a changelog and return a mapping with its contents"""
        ...

    @abc.abstractmethod
    def parse_changes(self, text: str) -> Iterable[Mapping[str, str]]:
        """Parse the changes and return a list of the changes

        Each change is represented using a mapping which needs to have at least a "type" and a "text" key!
        """
        ...

    @abc.abstractmethod
    def split_changelog(self, text: str) -> Tuple[str, str]:
        """Split a changelog into a tuple of its header and its changes"""
        ...

    @abc.abstractmethod
    def split_changelogs(self, text: str) -> Iterable[str]:
        """Split multiple changelogs in the same file into separate strings"""
        ...


def guess_parser(text: str) -> Parser:
    for _parser in _PARSERS:
        if _parser.can_handle(text):
            return _parser
    raise KeyError("No parser can handle this text", text)


ParserPType = Union[Type[Parser], Parser, str]


def get_parser(_parser: ParserPType) -> Parser:
    if isinstance(_parser, Parser):
        return _parser
    elif inspect.isclass(_parser) and issubclass(_parser, Parser):
        return _parser()
    elif isinstance(_parser, str):
        _parser = _parser.lower().strip()
        _parser = _ALIAS_MAP[_parser]
        return _parser

    raise ValueError(f"Can't find a parser based on {_parser}", _parser)


def register_parser(_parser: Type[Parser], alias: Iterable[str]) -> Parser:
    if not issubclass(_parser, Parser):
        raise SyntaxError(f"Parser must derive from {Parser} base class!", _parser)

    _parser = _parser()

    _names = []
    for name in alias:
        _name = name.lower().strip()
        if _name in _ALIAS_MAP:
            raise KeyError(f"Alias {name} already in use for {_ALIAS_MAP[_name]}", name)

        _ALIAS_MAP[_name] = _parser

        _names.append(_name)

    _parser.__ALIAS = list(_names)
    _PARSERS.add(_parser)

    return _parser


def parser(*names: str):
    return partial(register_parser, alias=names)


import_directory(Path(__file__), __package__)
