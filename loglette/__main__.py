#!/usr/bin/env python

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

from loglette import Changelog


def run(args: Namespace):
    changelog = Changelog.parse(args.file.read_text())
    print(changelog.format(args.format))


def main(*args):
    parser = ArgumentParser("Loglette", description="A tool to make changelogs easy or something like that")
    parser.add_argument("file", type=Path, help="The file you'd like to parse")
    parser.add_argument("-f", "--format", help="output format", default="markdown")

    args = parser.parse_args(args)
    run(args)


if __name__ == "__main__":
    main(*sys.argv)
