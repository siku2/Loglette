import re
from typing import Pattern

_WS = r"[ \t]*"

_HEADER_MATCHER = rf"^#{{2}}{_WS}\[.+?\](?:{_WS}-{_WS}.+?)?{_WS}$"
_FLAGS = re.MULTILINE

CHANGELOG_SPLITTER: Pattern = re.compile(rf"({_HEADER_MATCHER})", _FLAGS)
HEADER_SPLITTER: Pattern = re.compile(rf"({_HEADER_MATCHER})", _FLAGS)

_HEADER_PARSER = rf"^#{{2}}{_WS}\[(.+?)\](?:{_WS}-{_WS}(.+?))?{_WS}$"
HEADER_PARSER: Pattern = re.compile(_HEADER_PARSER, _FLAGS)

CHANGE_TYPE_MATCHER: Pattern = re.compile(rf"^#{{3}}{_WS}(.+?){_WS}$", _FLAGS)

CHANGES_PARSER: Pattern = re.compile(rf"^{_WS}[-*]{_WS}(.+?){_WS}$", _FLAGS)
