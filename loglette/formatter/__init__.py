import abc
from functools import partial
from pathlib import Path
from typing import Any, Sequence, Type

from ..changelog import Changelog
from ..utils import import_directory

_ALIAS_MAP = {}
_FORMATTERS = set()


class Formatter(abc.ABC):

    @abc.abstractmethod
    def format(self, changelog: Changelog, **options) -> Any:
        return changelog


def get_formatter(name: str) -> Formatter:
    name = name.lower().strip()
    formatter = _ALIAS_MAP[name]
    if not isinstance(formatter, Formatter):
        formatter = formatter()
        _ALIAS_MAP[name] = formatter
    return formatter


def register_formatter(formatter: Type[Formatter], alias: Sequence[str]):
    if not issubclass(formatter, Formatter):
        raise SyntaxError(f"Formatter must derive from {Formatter} base class!")

    _names = []
    for name in alias:
        _name = name.lower().strip()
        if _name in _ALIAS_MAP:
            raise KeyError(f"Alias {name} already in use for {_ALIAS_MAP[_name]}")

        _ALIAS_MAP[_name] = formatter

        _names.append(_name)

    formatter.__ALIAS = list(_names)
    _FORMATTERS.add(formatter)


def formatter(*names: str):
    return partial(register_formatter, alias=names)


import_directory(Path(__file__), __package__)
