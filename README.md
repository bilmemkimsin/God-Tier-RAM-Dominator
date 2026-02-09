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
- Write audit log + undo snapshot support in the core engine.
- Offline AI assistant panel (local LLM via Ollama-compatible API).
- Optional kernel driver sample (advanced / opt-in).

## Project Layout
```
core/        # memory ops, scanner, pointer scanner
ui/          # PySide6 UI
injector/    # DLL/agent placeholders
scripts/     # sample scripts
docs/        # documentation
demo_target/ # demo C++ target
kernel_driver/ # optional kernel RW driver sample
installer/  # Inno Setup script + build assets
```

## Quick Start (Windows)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m ui.app
```

> On non‑Windows platforms, memory access APIs are stubbed for safety and clarity. The mock engine is still fully testable.

## Installation (Tek Tık Kurulum)
### Son kullanıcı (önerilen)
1. **TitanRAM-Setup.exe** dosyasını indirin.
2. Çalıştırın ve sihirbazdaki seçenekleri tamamlayın.
3. Kurulum sonunda **“Programı şimdi başlat”** seçeneğini işaretleyin.

> Kernel modu tamamen opsiyoneldir ve yalnızca Advanced/God Mode ile etkinleştirilir.

### Geliştirici / Derleme (setup.exe üretimi)
TitanRAM için tercih edilen derleme yöntemi **pyside6-deploy (Nuitka)** ile `--onefile` modudur.

#### 1) Onefile EXE üret (tercih edilen)
```powershell
build.ps1 -Mode pyside6-deploy
```

#### 2) PyInstaller (alternatif)
```powershell
build.ps1 -Mode pyinstaller
```

#### 3) Inno Setup ile paketle
1. `dist/TitanRAM/` çıktısını `installer/TitanRAM.iss` dosyasının `Files` bölümünde belirtilen konuma yerleştirin.
2. `installer/third_party/` içine şu dosyaları koyun:
   - `python-3.12.x-embed-amd64.zip`
   - `get-pip.py`
3. `installer/TitanRAM.iss` dosyasını Inno Setup ile derleyin.

Detaylar için `installer/README.md` dosyasına bakın.

## Usage Overview
1. Launch TitanRAM.
2. Select a process from the left panel and attach.
3. Choose scan type and data type, run scans, and refine with next scan.
4. Inspect values in the center panel; right panel shows hex + disasm placeholders.
5. Add interesting addresses to watch list; run scripts in the console panel.

## Export/Automation
- `.ct` Cheat Engine table (basic export stub).
- JSON and C++ header exports for SDK‑style workflows.

## Safety & Ethics (Read This)
- **Default mode is user‑mode only** (OpenProcess + Read/WriteProcessMemory). Admin rights + SeDebugPrivilege cover most single‑player targets.
- **Kernel mode is optional and dangerous**. It is hidden behind an Advanced/God Mode concept and requires explicit user action.
- **Online/competitive games are off‑limits**. Anti‑cheat systems can detect kernel access and issue bans.
- **Educational use only**: reverse engineering, malware analysis, debugging, and single‑player modding.

TitanRAM **does not** include anti‑cheat bypasses or network attack tooling. Any attempt to use it against third‑party services or online games is forbidden. This project is a learning and research platform.

## Kernel Mode (Advanced / God Mode)
The optional kernel driver is provided for offline research on machines you control.

### Risks
- Kernel drivers can crash your system (BSOD risk).
- Driver Signature Enforcement must be disabled or test signing enabled.
- Modern anti‑cheat systems can detect kernel access and ban accounts.

### Test Signing (Recommended)
```powershell
bcdedit /set testsigning on
shutdown /r /t 0
```

### Driver İmzalama (Özet)
```powershell
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=TitanRAM Test" -CertStoreLocation Cert:\\LocalMachine\\My
$pwd = ConvertTo-SecureString -String "titanram" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath .\\TitanRAM.pfx -Password $pwd
"C:\\Program Files (x86)\\Windows Kits\\10\\bin\\x64\\signtool.exe" sign /f TitanRAM.pfx /p titanram /t http://timestamp.digicert.com TitanRAM.sys
```

### Temporary Signature Enforcement Disable
Advanced Startup → Troubleshoot → Startup Settings → **7. Disable driver signature enforcement**

### Build + Load (Overview)
- Install Visual Studio 2022 + WDK
- Build the driver in `kernel_driver/`
- Sign the driver with a test certificate
- Load with `sc.exe` or OSR Loader

See `kernel_driver/README.md` for a step‑by‑step walkthrough.

## Docs
See `docs/USAGE.md` for workflows and architecture notes.
