#!/usr/bin/env python3
"""news-image-20261118: write the front-page image to the output directory.

The image (entry.png, 1024x1024, "The World in One Day — Wednesday
18 November 2026") is bundled in this repository. This program only copies
it to $MAKEFUN_OUTPUT_DIR/entry.png (default /output), using the standard
library only, so both runs produce byte-identical output.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
