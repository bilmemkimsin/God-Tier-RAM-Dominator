# TitanRAM Kernel Driver (Optional / Advanced)

> **Danger Zone**: Kernel drivers can cause BSODs and destabilize your system. Use only for offline research on machines you control.

## Overview
This is a minimal read/write kernel driver sample for Windows 11 (2026-era). It is **optional** and **not enabled by default**. TitanRAM uses user-mode APIs by default.

## Build Prerequisites
- Windows 11
- Visual Studio 2022
- Windows Driver Kit (WDK) installed

## Build Steps
1. Open the driver project in Visual Studio (create a KMDF driver project and replace the `.c` with `src/driver.c`).
2. Set configuration to x64.
3. Build the driver to produce a `.sys` file.

## Test Signing (Recommended)
```powershell
bcdedit /set testsigning on
shutdown /r /t 0
```

Create and install a self-signed cert, then sign the driver:
```powershell
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=TitanRAM Test" -CertStoreLocation Cert:\LocalMachine\My
$pwd = ConvertTo-SecureString -String "titanram" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath .\TitanRAM.pfx -Password $pwd

# Sign with signtool (from Windows SDK)
"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe" sign /f TitanRAM.pfx /p titanram /t http://timestamp.digicert.com TitanRAM.sys
```

## Load Driver
```powershell
sc.exe create TitanRW type= kernel start= demand binPath= "C:\Path\To\TitanRAM.sys"
sc.exe start TitanRW
```

## Alternate (Temporary) Signature Enforcement Disable
Use Advanced Startup → Troubleshoot → Startup Settings → **7. Disable driver signature enforcement**.

## IOCTL Interface
The driver exposes a device `\\.\TitanRW` with two IOCTLs for read/write. See `src/driver.c` for structure definitions.

## Safety Notes
- Avoid BYOVD/vulnerable drivers (often blocked and high risk in 2026).
- Modern anti-cheat systems can detect kernel access and may ban accounts.
- Use only for offline, educational use.
