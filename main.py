#!/usr/bin/env python3
"""Write the 23 November 2026 front-page poster to the output directory.

Stdlib only. The poster lives in this repository as ``entry.png``; this
program checks it against the competition's limits and copies it to
``/output/entry.png`` (or to the directory given as the first argument).
It writes the same bytes on every run.
"""
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
OUTPUT_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
WANT_WIDTH = 1024
WANT_HEIGHT = 1024


def png_dimensions(data):
    """Return (width, height) from the IHDR chunk of a PNG byte string."""
    if data[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file (bad magic bytes)")
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ValueError("not a PNG file (missing IHDR chunk)")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def main(argv):
    out_dir = argv[1] if len(argv) > 1 else "/output"
    dest = os.path.join(out_dir, OUTPUT_NAME)

    with open(SOURCE, "rb") as handle:
        blob = handle.read()

    width, height = png_dimensions(blob)
    if (width, height) != (WANT_WIDTH, WANT_HEIGHT):
        raise SystemExit(
            f"entry.png is {width}x{height}, expected "
            f"{WANT_WIDTH}x{WANT_HEIGHT}"
        )
    if len(blob) > MAX_BYTES:
        raise SystemExit(
            f"entry.png is {len(blob)} bytes, over the {MAX_BYTES} byte limit"
        )

    os.makedirs(out_dir, exist_ok=True)
    with open(dest, "wb") as handle:
        handle.write(blob)
    os.chmod(dest, 0o644)

    # Read the copy back and confirm it is byte-identical to the source,
    # and that it stays world-readable for the grader to collect.
    with open(dest, "rb") as handle:
        written = handle.read()
    if written != blob:
        raise SystemExit("output does not match entry.png after copying")
    if os.stat(dest).st_mode & 0o777 != 0o644:
        raise SystemExit("output is not mode 0644")

    print(
        f"wrote {dest} ({width}x{height}, {len(blob)} bytes, "
        f"sha256 {sha256_hex(blob)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
