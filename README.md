# TitanRAM (God Tier RAM Dominator)

> **Educational/Research Use Only**
> TitanRAM is intended for reverse engineering, security research, malware analysis, debugging, and single‑player game modding. **Using it in online games or against software you do not own or have explicit permission to test can be illegal and will likely trigger bans or legal action.** You are responsible for complying with all laws and terms of service.

TitanRAM is a modern, modular memory analysis workstation built for power users. It ships with a dockable Qt6 UI, a high‑performance scanner core, a pointer chain analyzer, and an extensible scripting surface. Optional deep‑access features (agent DLL / driver) are designed as *opt‑in* components.

## Features (Implemented Core)
- Process enumeration + attach abstraction (cross‑platform; Windows memory access stubbed when not on Windows).
- God‑tier scanner engine (exact, increased/decreased/unchanged, float/double, string, AOB).
- Multi‑level pointer chain scanner (fast, filterable).
- Hex viewer/disassembler placeholders with clear extension points.
- PySide6 UI shell with dockable panels and cyber‑dark theme.
- Snapshot diff + value history data model.
- Export model definitions (CT/JSON/C++ header stubs).
- Scripting entrypoints for Python/Lua (stubs).

## Project Layout
```
core/        # memory ops, scanner, pointer scanner
ui/          # PySide6 UI
injector/    # DLL/agent placeholders
scripts/     # sample scripts
docs/        # documentation
demo_target/ # demo C++ target
```

## Quick Start (Windows)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m ui.app
```

> On non‑Windows platforms, memory access APIs are stubbed for safety and clarity. The mock engine is still fully testable.

## Usage Overview
1. Launch TitanRAM.
2. Select a process from the left panel and attach.
3. Choose scan type and data type, run scans, and refine with next scan.
4. Inspect values in the center panel; right panel shows hex + disasm placeholders.
5. Add interesting addresses to watch list; run scripts in the console panel.

## Export/Automation
- `.ct` Cheat Engine table (basic export stub).
- JSON and C++ header exports for SDK‑style workflows.

## Safety Notice
TitanRAM **does not** include anti‑cheat bypasses or network attack tooling. Any attempt to use it against third‑party services or online games is forbidden. This project is a learning and research platform.

## Docs
See `docs/USAGE.md` for workflows and architecture notes.
