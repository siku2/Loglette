from typing import Dict, List, Tuple

from . import pattern
from .. import Parser, parser


@parser("loglette")
class LogletteParser(Parser):
    @classmethod
    def parse_value(cls, value: str, text_style: str = None) -> str:
        if text_style:
            if text_style == "|":
                value = value.strip()
            elif text_style == ">":
                value = pattern.WHITESPACE_STRIPPER.sub(" ", value).strip()
            else:
                raise SyntaxError(f"Unknown text style ({text_style})")
        return value

    def parse_header(self, text: str) -> Dict[str, str]:
        headers = {}
        for match in pattern.HEADER_PARSER.finditer(text):
            key, text_style, value = match.groups(None)
            value = self.parse_value(value, text_style)
            headers[key] = value

        headers["release_date"] = headers.get("release")

        return headers

    def parse_changes(self, text: str) -> List[Dict[str, str]]:
        changes = []
        for match in pattern.CHANGES_PARSER.finditer(text):
            change_type, priority, text_style, value = match.groups(None)
            text = self.parse_value(value, text_style)

            change = {
                "type": change_type.upper(),
                "priority": priority,
                "text": text
            }

            changes.append(change)
        return changes

    @classmethod
    def split_changelog(cls, text: str) -> Tuple[str, str]:
        header, changes = pattern.HEADER_SPLITTER.split(text, maxsplit=1)
        return header, changes

    @classmethod
    def split_changelogs(cls, text: str) -> List[str]:
        return pattern.CHANGELOG_SPLITTER.split(text)
