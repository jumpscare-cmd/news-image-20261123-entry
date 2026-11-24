#!/usr/bin/env python3
"""Write entry.png to the output directory.

Usage: python3 main.py [OUTPUT_DIR]

The output directory is the first command-line argument when given,
otherwise the MAKEFUN_OUTPUT_DIR environment variable, otherwise this
script's own directory. The copied file is named entry.png, its mode is
set to 0644, and the copied bytes are verified against the source.
Standard library only; no network access.
"""

import hashlib
import os
import shutil
import sys


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(script_dir, "entry.png")

    if len(sys.argv) > 1:
        out_dir = sys.argv[1]
    elif os.environ.get("MAKEFUN_OUTPUT_DIR"):
        out_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    else:
        out_dir = script_dir

    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)

    with open(src, "rb") as f:
        src_bytes = f.read()
    with open(dst, "rb") as f:
        dst_bytes = f.read()
    if src_bytes != dst_bytes:
        raise SystemExit("error: copied bytes do not match the source")
    print("wrote %s (%d bytes, sha256 %s)"
          % (dst, len(dst_bytes),
             hashlib.sha256(dst_bytes).hexdigest()))


if __name__ == "__main__":
    main()
