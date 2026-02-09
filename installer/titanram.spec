# PyInstaller spec example for TitanRAM
# Build: pyinstaller installer/titanram.spec

from pathlib import Path

block_cipher = None

project_root = Path(__file__).resolve().parents[1]

analysis = Analysis(
    [str(project_root / "ui" / "app.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=[(str(project_root / "ui" / "theme.py"), "ui")],
    hiddenimports=["PySide6"],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(analysis.pure, analysis.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    analysis.scripts,
    analysis.binaries,
    analysis.zipfiles,
    analysis.datas,
    name="TitanRAM",
    console=False,
    icon=str(project_root / "installer" / "assets" / "titanram.ico"),
)

coll = COLLECT(
    exe,
    analysis.binaries,
    analysis.zipfiles,
    analysis.datas,
    name="TitanRAM",
)
