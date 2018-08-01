#!/usr/bin/env python

from argparse import ArgumentParser, Namespace
from pathlib import Path

from loglette import Version, parse


def run(args: Namespace):
    changelogs = parse(args.file.read_text(), parser=args.parser)

    # Check against presets using lowercase but make sure to preserve version tag!
    version = args.version
    version_str = version.lower()

    if version_str == "flatten":
        changelog = changelogs.flatten()
    elif version_str == "latest":
        changelog = changelogs.latest
    elif version_str == "first":
        changelog = changelogs.first
    else:
        target = Version.parse(version)
        changelog = changelogs[target]

    if changelog:
        print(changelog.format(args.format))
    else:
        print("Nothing to display")


def main(*args):
    args = args or None

    parser = ArgumentParser("loglette", description="A tool to make changelogs easy or something like that")
    parser.add_argument("file", type=Path, help="The file you'd like to parse")
    parser.add_argument("-p", "--parser", default=None, help="Specify the parser to use. By default Loglette tries to guess the correct parser")
    parser.add_argument("-f", "--format", default="markdown", help="output format")
    parser.add_argument("-v", "--version", default="first", help="How to parse multiple changelogs")

    args = parser.parse_args(args)
    run(args)


if __name__ == "__main__":
    main()
