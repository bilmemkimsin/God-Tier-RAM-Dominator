# TitanRAM Usage

## Core Workflow
1. Attach to a process.
2. Run a first scan (exact/unknown).
3. Change target values in the app/game.
4. Run a next scan (increased/decreased/changed).
5. Freeze or edit values, add to watch list.

## Architecture Notes
- `core/` houses memory abstraction, scanners, and pointer chains.
- `ui/` holds the dockable Qt shell.
- `injector/` is reserved for optional internal agent tooling.

## Scripting
Python and Lua entrypoints are intended for automation. See `scripts/` for examples.
