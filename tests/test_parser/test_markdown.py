from datetime import datetime
from pathlib import Path

from loglette import guess_parser, parse
from loglette.parser.markdown import MarkdownParser as parser

text = Path("tests/logs/keep-a-changelog.md").read_text("utf-8")


def test_pattern():
    changelogs = parse(text)
    assert len(changelogs) == 12

    changelog = changelogs.latest
    assert changelog.version == (1, 0, 0)
    assert changelog.release_date == datetime(2017, 6, 20)
    assert changelog.changes[0].text == "New visual identity by @tylerfortune8."
    assert changelog.changes[0].change_type == "ADDED"

    print(changelog.loglette())


def test_can_handle():
    assert parser.can_handle(text)


def test_right_guess():
    assert guess_parser(text) is parser
