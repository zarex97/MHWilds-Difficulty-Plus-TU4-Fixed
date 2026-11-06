# Monster Difficulty Plus TU4 (BETA v2): fixed files

An updated copy of [Monster Difficulty Plus - Updated for TU4 (Beta)](https://www.nexusmods.com/monsterhunterwilds/mods/566) by **RexZakel**. It repairs the Yian Kut-Ku and Blangonga files after Monster Hunter Wilds' August 2026 update.

The mod and its design belong to RexZakel, and this copy is shared with their permission. Please support the [original mod page](https://www.nexusmods.com/monsterhunterwilds/mods/566).

## What changed

Only these two files differ from version 1.42 of the mod:

- `natives/STM/GameDesign/Enemy/Em0008/00/Data/Em0008_00_Param_Legendary.user.3` (Yian Kut-Ku)
- `natives/STM/GameDesign/Enemy/Em0022/00/Data/Em0022_00_Param_Legendary.user.3` (Blangonga)

The game update added a field, `IsIgnoreActionAttackRate`, to `app.user_data.EmParamLegendary.ShellCustomData`. Both mod files still used the old layout.

Each file was rebuilt from the current game version of that file, then given the mod's one change: `MotionSpeedRate` goes from `1.05` to `1.1`. The new field keeps the game's value, `False`.

A stray Windows shortcut, `Em0156 - Shortcut.lnk`, was also left out. The game doesn't use it.

## Install

1. Install [REFramework](https://www.nexusmods.com/monsterhunterwilds/mods/93).
2. Launch the game, open the REFramework menu, and check **Enable Loose File Loader** in the LooseFileLoader section.
3. Close the game.
4. Download the zip from [Releases](../../releases/latest) and extract its `natives` folder into the game's base directory.

To uninstall, delete the `Enemy` folder inside `natives`.

## Status

The rebuilt files were checked against the game's current file layout. They have not yet been confirmed in a hunt, so please report any problems in [Issues](../../issues).

All players in a multiplayer session should use the same version of the mod. See the [original mod page](https://www.nexusmods.com/monsterhunterwilds/mods/566) for details.
