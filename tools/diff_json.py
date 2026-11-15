"""Lists every value that differs between two decoded .user.3 JSON trees.

usage: python3 tools/diff_json.py MOD_DIR VANILLA_DIR REL_PATH...
Prints one tab-separated line per difference: file, field path, vanilla value, mod value.
"""
import json
import os
import sys

MISSING = "<missing>"


def walk(path, vanilla, mod, out):
    if isinstance(vanilla, dict) and isinstance(mod, dict):
        for key in list(vanilla) + [k for k in mod if k not in vanilla]:
            walk(f"{path}.{key}" if path else key, vanilla.get(key, MISSING), mod.get(key, MISSING), out)
    elif isinstance(vanilla, list) and isinstance(mod, list):
        if len(vanilla) != len(mod):
            out.append((path + ".length", len(vanilla), len(mod)))
        for i in range(max(len(vanilla), len(mod))):
            walk(f"{path}[{i}]", vanilla[i] if i < len(vanilla) else MISSING, mod[i] if i < len(mod) else MISSING, out)
    elif path.endswith(".pad") and mod == MISSING:
        pass  # REasy reads Vec3 padding but does not keep it
    elif vanilla != mod:
        out.append((path, vanilla, mod))


def main():
    mod_dir, vanilla_dir = sys.argv[1], sys.argv[2]
    for rel in sys.argv[3:]:
        with open(os.path.join(vanilla_dir, rel), encoding="utf-8") as f:
            vanilla = json.load(f)
        with open(os.path.join(mod_dir, rel), encoding="utf-8") as f:
            mod = json.load(f)
        out = []
        walk("", vanilla, mod, out)
        for path, v, m in out:
            print(f"{rel}\t{path}\t{json.dumps(v)}\t{json.dumps(m)}")


if __name__ == "__main__":
    main()
