from loglette.parser.loglette import LogletteParser as parser
from tests import example_test


def test_text_style():
    examples = {
        ("\tthis a test\n\t\ttest ", None): "\tthis a test\n\t\ttest ",
        ("\tthis a test\n\t\ttest ", "|"): "this a test\n\t\ttest",
        ("\tthis a test\n\t\ttest ", ">"): "this a test test",
        ("\tthis a test\n\t\ttest ", "!"): SyntaxError("Unknown text style (!)")
    }

    example_test(parser.parse_value, examples)


def test_split_changelog():
    examples = {
        ("head\n---\nbody",): ("head", "body"),
        ("head\n---\n---\nbody",): ("head", "---\nbody"),
        ("head\nbody",): ValueError("not enough values to unpack (expected 2, got 1)"),
        ("head---body",): ValueError("not enough values to unpack (expected 2, got 1)")
    }

    example_test(parser.split_changelog, examples)
