#!/usr/bin/env python3
"""Copy entry.png to the output directory, verifying integrity.

Stdlib only. Default output dir is /output; pass a different directory
as the first argument, e.g. ``python3 main.py /tmp/out``.
"""
import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # 1 MiB limit
OUTPUT_NAME = "entry.png"


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "/output"
    out_path = os.path.join(out_dir, OUTPUT_NAME)

    if not os.path.isfile(SOURCE):
        raise SystemExit(f"source not found: {SOURCE}")

    with open(SOURCE, "rb") as f:
        data = f.read()

    if data[:8] != PNG_SIGNATURE:
        raise SystemExit("entry.png is not a valid PNG (bad signature)")
    if len(data) > MAX_BYTES:
        raise SystemExit(
            f"entry.png is {len(data)} bytes, over the {MAX_BYTES} byte limit"
        )

    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)

    # Verify the copy byte-for-byte.
    with open(out_path, "rb") as f:
        copied = f.read()
    if copied != data:
        raise SystemExit("copied file does not match entry.png")

    os.chmod(out_path, 0o644)
    print(f"wrote {out_path} ({len(data)} bytes, md5 {md5_of(out_path)})")


if __name__ == "__main__":
    main()
