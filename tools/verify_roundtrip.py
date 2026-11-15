"""Checks that REasy rebuilds each .user.3 file byte for byte from its parse.

A byte-identical rebuild means every field was read with the right type and size,
so the JSON from decode_user3.py describes the whole file.

usage: python3 tools/verify_roundtrip.py REASY_DIR RSZ_SCHEMA FILE...
"""
import sys

import reasy_loader


def main():
    reasy_dir, schema = sys.argv[1:3]
    TypeRegistry, RszFile, _ = reasy_loader.load(reasy_dir)
    registry = TypeRegistry(schema)

    failures = 0
    for path in sys.argv[3:]:
        with open(path, "rb") as f:
            original = f.read()
        rebuilt = bytes(reasy_loader.read_user_file(RszFile, registry, path).build())
        if rebuilt == original:
            print(f"identical  {path}")
        else:
            failures += 1
            print(f"DIFFERENT  {path} ({len(original)} -> {len(rebuilt)} bytes)")

    print(f"{len(sys.argv) - 3 - failures} identical, {failures} different")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
