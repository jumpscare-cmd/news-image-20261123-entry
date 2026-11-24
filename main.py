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
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def validate_png(path):
    """Refuse anything that is not the expected 1024x1024 PNG."""
    with open(path, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        raise SystemExit("error: %s is %d bytes, over the 1 MiB limit"
                         % (path, len(data)))
    if not data.startswith(PNG_SIGNATURE):
        raise SystemExit("error: %s does not start with the PNG signature"
                         % path)
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise SystemExit("error: %s has no IHDR chunk" % path)
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit("error: %s is %dx%d, expected %dx%d"
                         % (path, width, height,
                            EXPECTED_WIDTH, EXPECTED_HEIGHT))
    return data


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(script_dir, "entry.png")

    if len(sys.argv) > 1:
        out_dir = sys.argv[1]
    elif os.environ.get("MAKEFUN_OUTPUT_DIR"):
        out_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    else:
        out_dir = script_dir

    validate_png(src)

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
