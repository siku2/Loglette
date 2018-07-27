#!/usr/bin/env python

from argparse import ArgumentParser, Namespace
from pathlib import Path

from loglette import ChangelogRange


def run(args: Namespace):
    changelogs = ChangelogRange.parse(args.file.read_text())
    print(changelogs.last.format(args.format))


def main(*args):
    args = args or None

    parser = ArgumentParser("loglette", description="A tool to make changelogs easy or something like that")
    parser.add_argument("file", type=Path, help="The file you'd like to parse")
    parser.add_argument("-f", "--format", help="output format", default="markdown")

    args = parser.parse_args(args)
    run(args)


if __name__ == "__main__":
    main()
