"""Decodes the mod's .user.3 files into JSON under source/.

The JSON layout follows https://github.com/dtlnor/MHWs-in-json, so each file can be
compared with the game's own data there. Enum values are written as "[value]NAME".

usage: python3 tools/decode_user3.py REASY_DIR RSZ_SCHEMA ENUMS_JSON OUT_DIR FILE...
  REASY_DIR   folder holding REasy's file_handlers and utils
  RSZ_SCHEMA  rszmhwilds.json from https://github.com/dtlnor/RE_RSZ
  ENUMS_JSON  Enums_Internal.json from https://github.com/dtlnor/MHWs-in-json
"""
import json
import os
import struct
import sys

import reasy_loader


def shortest_float32(value):
    """Shortest decimal that reads back as the same 32-bit float (1.05, not 1.0499999523)."""
    bits = struct.pack("<f", value)
    for digits in range(1, 10):
        text = f"{value:.{digits}g}"
        if struct.pack("<f", float(text)) == bits:
            return float(text)
    return value


class EnumNames:
    def __init__(self, path):
        with open(path, encoding="utf-8") as f:
            self.by_type = json.load(f)

    def lookup(self, enum_type):
        return self.by_type.get(enum_type)

    def for_serializable(self, owner_type):
        """app.X.ENUM_Serializable stores _Value as the hashed ENUM_Fixed value when that enum exists."""
        base = owner_type.removesuffix("_Serializable")
        return self.lookup(base + "_Fixed") or self.lookup(base)

    @staticmethod
    def format(value, names):
        """[value]NAME, or [value]A|B|C for bit flags, in declaration order."""
        for name, v in names.items():
            if v == value:
                return f"[{value}]{name}"
        flags = [name for name, v in names.items() if v > 0 and v & (v - 1) == 0 and value & v == v]
        if flags and sum(names[n] for n in flags) == value:
            return f"[{value}]" + "|".join(flags)
        return value


class Decoder:
    def __init__(self, rsz, registry, enums, data_types):
        self.rsz = rsz
        self.registry = registry
        self.enums = enums
        self.dt = data_types

    def type_name(self, instance_id):
        info = self.registry.get_type_info(self.rsz.instance_infos[instance_id].type_id)
        return info["name"]

    def instance(self, instance_id):
        name = self.type_name(instance_id)
        userdata = self.rsz._rsz_userdata_dict.get(instance_id)
        if userdata is not None:
            return {name: {"userdataPath": self.rsz.get_rsz_userdata_string(userdata)}}

        serializable_names = self.enums.for_serializable(name) if name.endswith("_Serializable") else None
        fields = {}
        for field, data in self.rsz.parsed_elements.get(instance_id, {}).items():
            if field == "_Value" and serializable_names:
                names = serializable_names
            else:
                names = self.enums.lookup(getattr(data, "orig_type", ""))
            fields[field] = self.enum_value(data, names) if names else self.value(data)
        return {name: fields}

    def enum_value(self, data, names):
        if isinstance(data, self.dt.ArrayData):
            return [self.enum_value(item, names) for item in data.values]
        return EnumNames.format(data.value, names)

    def value(self, data):
        dt = self.dt
        if isinstance(data, dt.ArrayData):
            return [self.value(item) for item in data.values]
        if isinstance(data, dt.StructData):
            return [{k: self.value(v) for k, v in item.items()} for item in data.values]
        if isinstance(data, (dt.UserDataData, dt.ObjectData)):
            # A null reference is written as {"": {}}, as in MHWs-in-json.
            return self.instance(data.value) if data.value else {"": {}}
        if isinstance(data, dt.F32Data):
            return shortest_float32(data.value)
        if isinstance(data, dt.GuidData):
            return data.guid_str
        if isinstance(data, dt.RawBytesData):
            return data.raw_bytes.hex()
        if hasattr(data, "value"):
            return data.value
        for attrs in (("x", "y", "z", "w"), ("x", "y", "z"), ("x", "y"), ("r", "g", "b", "a"), ("min", "max")):
            if all(hasattr(data, a) for a in attrs):
                return {a: self.scalar(getattr(data, a)) for a in attrs}
        raise TypeError(f"unhandled RSZ value type {type(data).__name__}")

    @staticmethod
    def scalar(v):
        return shortest_float32(v) if isinstance(v, float) else v


def main():
    reasy_dir, schema, enums_path, out_dir = sys.argv[1:5]
    TypeRegistry, RszFile, data_types = reasy_loader.load(reasy_dir)
    registry = TypeRegistry(schema)
    enums = EnumNames(enums_path)

    for path in sys.argv[5:]:
        rsz = reasy_loader.read_user_file(RszFile, registry, path)
        decoder = Decoder(rsz, registry, enums, data_types)
        tree = [decoder.instance(root) for root in rsz.object_table]

        out = os.path.join(out_dir, os.path.normpath(path) + ".json")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            json.dump(tree, f, indent=4, ensure_ascii=False)
            f.write("\n")
        print(out)


if __name__ == "__main__":
    main()
