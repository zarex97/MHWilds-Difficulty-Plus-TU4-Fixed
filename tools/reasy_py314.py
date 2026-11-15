"""Rewrites a copy of REasy's sources so they run on Python 3.14.

REasy uses two Python 3.15 features:
- "lazy" imports. Top-level ones move to the end of the module, so their names are bound
  when a function first runs, as a lazy import would bind them. Indented ones become plain.
- "return out.take_bytes()" on a local bytearray, which becomes "return bytes(out)".

usage: python3 tools/reasy_py314.py REASY_COPY_DIR
"""
import pathlib
import re
import sys

TOP_LEVEL_LAZY = re.compile(r"lazy ((?:from|import) .*\n?)")
INDENTED_LAZY = re.compile(r"^(\s+)lazy ((?:from|import) )")
TAKE_BYTES = re.compile(r"return (\w+)\.take_bytes\(\)")


def convert(source):
    source = TAKE_BYTES.sub(r"return bytes(\1)", source)
    lines = source.splitlines(keepends=True)
    kept, deferred = [], []
    i = 0
    while i < len(lines):
        match = TOP_LEVEL_LAZY.match(lines[i])
        if not match:
            kept.append(INDENTED_LAZY.sub(r"\1\2", lines[i]))
            i += 1
            continue
        statement = [match.group(1)]
        depth = lines[i].count("(") - lines[i].count(")")
        while depth > 0:  # parenthesized import over several lines
            i += 1
            statement.append(lines[i])
            depth += lines[i].count("(") - lines[i].count(")")
        deferred.extend(statement)
        i += 1

    result = "".join(kept)
    if deferred:
        if not result.endswith("\n"):
            result += "\n"
        result += "\n# imports that are lazy in Python 3.15\n" + "".join(deferred)
    return result


def main():
    for path in pathlib.Path(sys.argv[1]).rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        converted = convert(source)
        if converted != source:
            path.write_text(converted, encoding="utf-8")


if __name__ == "__main__":
    main()
