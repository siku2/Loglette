import importlib
from pathlib import Path
from typing import List


def import_directory(directory: Path, package: str, exclude: List[Path] = None):
    exclude = exclude or []
    if directory.is_file():
        exclude.append(directory)
        directory = directory.parent

    content = directory.glob("*")
    for pkg in content:
        if pkg in exclude:
            continue
        importlib.import_module("." + pkg.stem, package=package)
