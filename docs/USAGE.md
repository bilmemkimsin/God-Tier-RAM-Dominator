# TitanRAM Usage

## Core Workflow
1. Attach to a process.
2. Run a first scan (exact/unknown).
3. Change target values in the app/game.
4. Run a next scan (increased/decreased/changed).
5. Freeze or edit values, add to watch list.

## Write Auditing
All memory writes should be logged and paired with an undo snapshot in the core engine. This enables safer experimentation and rollback.

## Architecture Notes
- `core/` houses memory abstraction, scanners, and pointer chains.
- `ui/` holds the dockable Qt shell.
- `injector/` is reserved for optional internal agent tooling.
- `kernel_driver/` contains an optional read/write driver sample (advanced usage).

## Safety
- TitanRAM defaults to **user-mode** operations only (OpenProcess + Read/WriteProcessMemory).
- Kernel mode is opt-in and should be enabled only for offline research on your own systems.
- Every memory write should be treated as a potentially ToS-violating action depending on the target software.

## Scripting
Python and Lua entrypoints are intended for automation. See `scripts/` for examples.
