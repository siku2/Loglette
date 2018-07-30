from .__info__ import *
from .changelog import Changelog, ChangelogRange
from .formatter import Formatter, formatter, get_formatter
from .parser import Parser, get_parser, guess_parser, parser
from .version import Version


def parse(text: str) -> ChangelogRange:
    return ChangelogRange.parse(text)
