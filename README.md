# Monster Difficulty Plus TU4 (BETA v2): fixed files

An updated copy of [Monster Difficulty Plus - Updated for TU4 (Beta)](https://www.nexusmods.com/monsterhunterwilds/mods/566) by **RexZakel**. It repairs the Yian Kut-Ku and Blangonga files after Monster Hunter Wilds' August 2026 update. NexusMod auto-guard gave a false positive for the files and they haven't answered me. So I am uploading this to GitHub. https://www.nexusmods.com/monsterhunterwilds/mods/5285

I tried contacting RexZakel, but got no answer fromPlease support the [original mod page](https://www.nexusmods.com/monsterhunterwilds/mods/566).

## What changed

Only these two files differ from version 1.42 of the mod (Latest version from **RexZakel**):

- `natives/STM/GameDesign/Enemy/Em0008/00/Data/Em0008_00_Param_Legendary.user.3` (Yian Kut-Ku)
- `natives/STM/GameDesign/Enemy/Em0022/00/Data/Em0022_00_Param_Legendary.user.3` (Blangonga)

The `source` folder has every mod file decoded to JSON, in the same layout as the game data in [dtlnor/MHWs-in-json](https://github.com/dtlnor/MHWs-in-json), so each file can be compared with the game's own version. Compared with game version 1.040.02, the mod changes two things:

- `EmCommonDifficulty2.user.3`: in 183 of the 184 difficulty rows, `_Health` and `_PartsVital` are multiplied by 1.25 and `_ScarNormalAndTear` and `_ScarRaw` by 1.55, rounded to two decimals.
- `MotionSpeedRate` is raised for Rathian, Gravios, Yian Kut-Ku, Gypceros, Congalala, Blangonga, Nerscylla, Lala Barina, Rey Dau and Hirabami.

The other files match the game's data. The JSON comes from `tools/decode_user3.py`, which reads the files with the RSZ parser from [REasy](https://github.com/seifhassine/REasy) and the type list `rszmhwilds.json` from [dtlnor/RE_RSZ](https://github.com/dtlnor/RE_RSZ). `tools/verify_roundtrip.py` checks that REasy rebuilds each file byte for byte from what it read, and `tools/diff_json.py` lists the differences between two decoded folders. To decode again with Python 3.14:

```
git clone --depth 1 --filter=blob:none --sparse https://github.com/seifhassine/REasy.git
git -C REasy sparse-checkout set file_handlers utils
mkdir reasy && cp -r REasy/file_handlers REasy/utils reasy/
python3 tools/reasy_py314.py reasy
curl -LO https://raw.githubusercontent.com/dtlnor/RE_RSZ/MHWilds/rszmhwilds.json
curl -LO https://raw.githubusercontent.com/dtlnor/MHWs-in-json/main/Enums_Internal.json
python3 tools/verify_roundtrip.py reasy rszmhwilds.json $(git ls-files 'natives/*.user.3')
python3 tools/decode_user3.py reasy rszmhwilds.json Enums_Internal.json source $(git ls-files 'natives/*.user.3')
```


## Install

1. Install [REFramework](https://www.nexusmods.com/monsterhunterwilds/mods/93).
2. Launch the game, open the REFramework menu, and check **Enable Loose File Loader** in the LooseFileLoader section.
3. Close the game.
4. Download the zip from [Releases](../../releases/latest) and extract its `natives` folder into the game's base directory.

To uninstall, delete the `Enemy` folder inside `natives`.

## Status

All players in a multiplayer session should use the same version of the mod. See the [original mod page](https://www.nexusmods.com/monsterhunterwilds/mods/566) for details.
## Shout outs
Given that this is just a fix of a previous mod, basically all credits goes towards RexZakel!
Rex, if you would like me to take down this mod please just say it!
## Possible updates on the future
I am thinking of adding customized sliders so you can adjust values as you see fit. I am also thinking of making monsters a bit faster, more powerful and tougher based on hp%, that should also help escalate difficulty. 
