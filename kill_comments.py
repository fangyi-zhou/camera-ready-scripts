#!/usr/bin/env python3

import re
import sys
from typing import List

COMMENT = re.compile(r"((?<!\\)|(?<=\\\\))%.*$")


def remove_comments(content: str) -> str:
    lines = []  # type: List[str]
    for line in content.splitlines():
        lines.append(COMMENT.sub("%", line))
    return "\n".join(lines)


if __name__ == "__main__":
    for file in sys.argv[1:]:
        print("Removing comments in %s" % file)
        with open(file) as f:
            content = f.read()
        removed = remove_comments(content)
        with open(file, "w") as f:
            f.write(removed)
