"""Reads a fls file (produced when using `-recorder` option, by default if you
use `latexmk`), and finds the files that are used during compilation that are
relative to the `fls` file.
These files include auxiliary files, but most likely includes all files you'll
need to producing a zip file.
"""

import re
import os
import sys
from typing import List, Set


def input_files_from_fls(tex_dir: str, lines: List[str]) -> Set[str]:
    files = set()  # type: Set[str]
    for line in lines:
        if line.startswith("INPUT "):
            file = line.split(" ")[1]
            if not os.path.isabs(file):
                file = os.path.join(tex_dir, file)
            files.add(file)
    return files


def find_files_in_dir(dir_to_keep: str, files: Set[str]) -> Set[str]:
    files_in_dir = set()  # type: Set[str]
    for file in files:
        rel_path = os.path.relpath(file, start=dir_to_keep)
        if not rel_path.startswith(".."):
            files_in_dir.add(rel_path)
    return files_in_dir


if __name__ == "__main__":
    tex_dir = os.path.realpath(os.path.dirname(sys.argv[1]))
    with open(sys.argv[1]) as f:
        fls = f.read().splitlines()
    input_files = input_files_from_fls(tex_dir, fls)
    files_to_zip = find_files_in_dir(tex_dir, input_files)
    print(*list(sorted(files_to_zip)))
