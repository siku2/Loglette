import re
from typing import Pattern

TEXT_STYLES = (">", "|")

_SPLITTER = r"(?:\n|^){char}{{3,}}(?:\n|$)"
HEADER_SPLITTER: Pattern = re.compile(_SPLITTER.format(char="-"))
CHANGELOG_SPLITTER: Pattern = re.compile(_SPLITTER.format(char="="))

_WS = r"[ \t]*"
_LINE_PARSER = rf"^{_WS}(?<!//){_WS}{{line}};$"
_META_VALUE = r"\[({content})\]"
_KEY = r"[a-zA-Z_]+"
_TXT_STYLE = "[" + "".join(TEXT_STYLES) + "]"
_TXT_VALUE = rf"(?:({_TXT_STYLE})\s?)?(.+?)"

_PRIORITY_META = _META_VALUE.format(content=r"\d+")
_PADDED_COLON = rf"{_WS}:{_WS}"

_PARSER_FLAGS = re.S | re.M
LINE_PARSER: Pattern = re.compile(_LINE_PARSER.format(line=_TXT_VALUE), _PARSER_FLAGS)
HEADER_PARSER: Pattern = re.compile(_LINE_PARSER.format(line=rf"({_KEY}){_PADDED_COLON}{_TXT_VALUE}"), _PARSER_FLAGS)
CHANGES_PARSER: Pattern = re.compile(_LINE_PARSER.format(line=rf"({_KEY})(?:{_PRIORITY_META})?{_PADDED_COLON}{_TXT_VALUE}"), _PARSER_FLAGS)

WHITESPACE_STRIPPER: Pattern = re.compile(r"\s+")
