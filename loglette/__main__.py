#!/usr/bin/env python

from argparse import ArgumentParser, Namespace
from pathlib import Path

from loglette import ChangelogRange, Version


def run(args: Namespace):
    changelogs = ChangelogRange.parse(args.file.read_text())
    version = args.version
    if version == "flatten":
        changelog = changelogs.flatten()
    elif version == "latest":
        changelog = changelogs.latest
    elif version == "first":
        changelog = changelogs.first
    else:
        target = Version.parse(version)
        changelog = changelogs[target]
    print(changelog.format(args.format))


def main(*args):
    args = args or None

    parser = ArgumentParser("loglette", description="A tool to make changelogs easy or something like that")
    parser.add_argument("file", type=Path, help="The file you'd like to parse")
    parser.add_argument("-f", "--format", default="markdown", help="output format")
    parser.add_argument("-v", "--version", choices=("flatten", "latest", "first"), default="first", help="How to parse multiple changelogs")

    args = parser.parse_args(args)
    run(args)


if __name__ == "__main__":
    main()
