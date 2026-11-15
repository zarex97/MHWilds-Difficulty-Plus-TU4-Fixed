"""Imports REasy's RSZ parser (https://github.com/seifhassine/REasy, MIT) for the other tools.

REasy targets Python 3.15. Run tools/reasy_py314.py on a copy of its file_handlers and
utils folders first when using Python 3.14; the two 3.15 builtins it needs are added here.
"""
import builtins
import sys
import types


class _Sentinel:
    """Stand-in for the Python 3.15 sentinel() builtin (PEP 661)."""

    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return self._name


class _FrozenDict(dict):
    """Stand-in for the Python 3.15 frozendict builtin (PEP 814)."""

    def __hash__(self):
        return hash(frozenset(self.items()))

    def _read_only(self, *args, **kwargs):
        raise TypeError("frozendict is immutable")

    __setitem__ = __delitem__ = update = pop = popitem = clear = setdefault = _read_only


def _stub_mmh3():
    """REasy imports mmh3 for scn.19 hashing, which .user files never use."""
    module = types.ModuleType("mmh3")

    def unavailable(*args, **kwargs):
        raise RuntimeError("mmh3 is not installed")

    module.hash = module.hash128 = module.hash_bytes = unavailable
    return module


def load(reasy_dir):
    if not hasattr(builtins, "sentinel"):
        builtins.sentinel = _Sentinel
    if not hasattr(builtins, "frozendict"):
        builtins.frozendict = _FrozenDict
    try:
        import mmh3  # noqa: F401
    except ImportError:
        sys.modules["mmh3"] = _stub_mmh3()

    sys.path.insert(0, reasy_dir)
    from utils.type_registry import TypeRegistry
    from file_handlers.rsz.rsz_file import RszFile
    from file_handlers.rsz import rsz_data_types
    return TypeRegistry, RszFile, rsz_data_types


def read_user_file(RszFile, registry, path):
    rsz = RszFile()
    rsz.type_registry = registry
    rsz.filepath = path
    rsz.game_version = "MHWILDS"
    with open(path, "rb") as f:
        rsz.read(f.read())
    return rsz
