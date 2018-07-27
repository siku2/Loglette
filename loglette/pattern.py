import re
from typing import Pattern

HEADER_SPLITTER: Pattern = re.compile(r"(?:\n|^)-{3,}(?:\n|$)")
CHANGELOG_SPLITTER: Pattern = re.compile(r"(?:\n|^)={3,}(?:\n|$)")

HEADER_PARSER: Pattern = re.compile(r"^[ \t]*(\w+)\s*:[ \t]*([>|])?\s*(.+?);$", re.S | re.M)
CHANGES_PARSER: Pattern = re.compile(r"^[ \t]*(?<!//)[ \t]*(\w+)(?:\[(\d+)\])?:\s*([>|])?\s*(.+?);$", re.S | re.M)

WHITESPACE_STRIPPER: Pattern = re.compile(r"\s+")
