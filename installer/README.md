# Installer Build (Windows)

This folder contains the Inno Setup script and build notes for producing a single `setup.exe`.

## Files
- `TitanRAM.iss` — Inno Setup script (wizard, tasks, install/uninstall actions).
- `titanram.spec` — PyInstaller spec example for building the UI executable.
- `third_party/` — place third-party archives/files here:
  - `python-3.12.x-embed-amd64.zip`
  - `get-pip.py`
- `assets/` — optional installer images/icons.

## Build Steps (Summary)
1. Build the app executable with PyInstaller.
2. Place the resulting `dist/TitanRAM/` into the location referenced by `TitanRAM.iss` (default: `dist/TitanRAM/`).
3. Place the embedded Python zip and `get-pip.py` into `installer/third_party/`.
4. Place the built `TitanRAM.sys` into `installer/` (or update `TitanRAM.iss` to the correct path).
5. Open `TitanRAM.iss` in Inno Setup and build.

## Notes
- The installer can enable test signing and install the driver **only if** the user opts in.
- Uninstall removes the driver and deletes the installed files.
