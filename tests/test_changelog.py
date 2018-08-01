from datetime import datetime
from pathlib import Path

from loglette import Version
from loglette.changelog import Changelog, ChangelogRange


def test_version_range():
    vrange = ChangelogRange.parse(Path("tests/logs/range.log").read_text())
    assert vrange is not vrange.copy()
    assert len(vrange) == 3
    assert len(vrange.flatten()) == 4
    assert vrange.get((6,)).changes[0].text == "sorting logs"
    assert len(vrange[(2, 0, 0):(5, 5, 1)]) == 2
    assert vrange.first.version == (5,)
    assert vrange.last.version == (3,)
    assert vrange.latest.version == (6,)
    assert vrange.oldest.version == (3,)


def test_spec():
    changelog = Changelog.parse(Path("tests/logs/spec.log").read_text())

    assert changelog.release_date == datetime(2018, 6, 28)
    assert changelog.version == Version(1, 0, 0, tag="dev")

    tests = [
        ("ADDED", "Keeping fullscreen when automatically switching to next episode", 10),
        ("CHANGED", "Showing \"new episode\" when there's actually a new episode "
                    "compared to last time and showing \"unseen episode\" when "
                    "there are unseen episodes", 0),
        ("FIXED", "Autoplay from the second last to the last episode works now", 0),
        ("DEPRECATED", "test\n//this isn't a comment because it's in the text!\n"
                       "               ####\n                    Almost\n"
                       "                     ASCII\n                       Art\n"
                       "               ####", 0),
        ("THIS", "isn't", 599999)

    ]

    for i, (kind, text, priority) in enumerate(tests):
        change = changelog.changes[i]
        assert change.change_type == kind
        assert change.text == text
        assert change.priority == priority

    loglette = changelog.loglette()
    assert Changelog.parse(loglette).loglette() == loglette
