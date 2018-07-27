from datetime import datetime
from typing import Dict, List, Tuple

from dateutil.parser import parser as DateParser

from . import pattern

date_parser = DateParser()


def parse_date(value: str) -> datetime:
    return date_parser.parse(value)


def parse_value(value: str, text_style: str = None) -> str:
    if text_style:
        if text_style == "|":
            value = value.strip()
        elif text_style == ">":
            value = pattern.WHITESPACE_STRIPPER.sub(" ", value)
        else:
            raise SyntaxError(f"Unknown text style ({text_style})")
    return value


def parse_header(text: str) -> Dict[str, str]:
    headers = {}
    for match in pattern.HEADER_PARSER.finditer(text):
        key, text_style, value = match.groups(None)
        value = parse_value(value, text_style)
        headers[key] = value

    return headers


def parse_changes(text: str) -> List[Dict[str, str]]:
    changes = []
    for match in pattern.CHANGES_PARSER.finditer(text):
        change_type, priority, text_style, value = match.groups(None)
        text = parse_value(value, text_style)

        change = {
            "type": change_type.upper(),
            "priority": priority,
            "text": text
        }

        changes.append(change)
    return changes


def split_changelog(text: str) -> Tuple[str, str]:
    header, changes = pattern.HEADER_SPLITTER.split(text, maxsplit=1)
    return header, changes


def split_changelogs(text: str) -> List[str]:
    return pattern.CHANGELOG_SPLITTER.split(text)
