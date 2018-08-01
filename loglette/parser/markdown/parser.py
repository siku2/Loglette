from typing import Dict, List, Tuple

from . import pattern
from .. import Parser, parser


@parser("markdown", "md")
class MarkdownParser(Parser):
    def parse_header(self, text: str) -> Dict[str, str]:
        match = pattern.HEADER_PARSER.match(text)
        version, release_date = match.groups(None)
        headers = {
            "version": version,
            "release_date": release_date
        }
        return headers

    def parse_changes(self, text: str) -> List[Dict[str, str]]:
        changes = []
        change_types = pattern.CHANGE_TYPE_MATCHER.split(text)[1:]
        for i in range(0, len(change_types) - 1, 2):
            change_type, _changes = change_types[i:i + 2]
            change_type = change_type.upper()

            for match in pattern.CHANGES_PARSER.finditer(_changes):
                text = match.group(1)

                change = {
                    "type": change_type,
                    "priority": 0,
                    "text": text
                }

                changes.append(change)
        return changes

    @classmethod
    def split_changelog(cls, text: str) -> Tuple[str, str]:
        _, header, changes = pattern.HEADER_SPLITTER.split(text, maxsplit=1)
        return header, changes

    @classmethod
    def split_changelogs(cls, text: str) -> List[str]:
        parts = pattern.CHANGELOG_SPLITTER.split(text)[1:]
        return ["".join(parts[i:i + 2]) for i in range(0, len(parts), 2)]
