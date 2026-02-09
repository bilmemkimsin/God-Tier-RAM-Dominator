; TitanRAM Inno Setup Script
#define MyAppName "TitanRAM"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "TitanRAM Project"
#define MyAppExeName "TitanRAM.exe"

[Setup]
AppId={{A7C2A3B4-7B0C-4C52-9D0A-9D4B55FA0E7B}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=output
<<<<<< codex/design-ultra-powerful-memory-analysis-tool-kadqva
OutputBaseFilename=TitanRAM-Setup
=======
OutputBaseFilename=TitanRAM_Setup
>>>>>> main
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "Masaüstü kısayolu oluştur"; GroupDescription: "Kısayollar"; Flags: unchecked
Name: "startmenuicon"; Description: "Başlat menüsü kısayolu oluştur"; GroupDescription: "Kısayollar"; Flags: checked
Name: "installpython"; Description: "Python'u kur (yüklü değilse)"; GroupDescription: "Python"; Flags: checked
Name: "installpackages"; Description: "Gerekli Python paketlerini otomatik kur"; GroupDescription: "Python"; Flags: checked
Name: "enabletestsigning"; Description: "Kernel modu için Test Signing etkinleştir (restart gerekir)"; GroupDescription: "Kernel"; Flags: unchecked
Name: "installkernel"; Description: "Kernel driver'ı yükle ve başlat (yalnızca test signing açıksa)"; GroupDescription: "Kernel"; Flags: unchecked

[Files]
Source: "..\dist\TitanRAM\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "third_party\python-3.12.x-embed-amd64.zip"; DestDir: "{app}\python"; Flags: ignoreversion
Source: "third_party\get-pip.py"; DestDir: "{app}\python"; Flags: ignoreversion
Source: "..\kernel_driver\README.md"; DestDir: "{app}\kernel_driver"; Flags: ignoreversion
Source: "..\kernel_driver\src\driver.c"; DestDir: "{app}\kernel_driver\src"; Flags: ignoreversion
<<<<<< codex/design-ultra-powerful-memory-analysis-tool-kadqva
Source: "..\kernel_driver\TitanRAM.sys"; DestDir: "{app}\kernel_driver"; Flags: ignoreversion; Check: FileExists(ExpandConstant('{src}\\..\\kernel_driver\\TitanRAM.sys'))
=======
>>>>>> main

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startmenuicon
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Programı şimdi başlat"; Flags: nowait postinstall skipifsilent

; Install embedded Python and pip
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; \
    Parameters: "-ExecutionPolicy Bypass -Command \"Expand-Archive -Path '{app}\\python\\python-3.12.x-embed-amd64.zip' -DestinationPath '{app}\\python\\embedded' -Force\""; \
<<<<<< codex/design-ultra-powerful-memory-analysis-tool-kadqva
    Tasks: installpython; Check: FileExists(ExpandConstant('{app}\\python\\python-3.12.x-embed-amd64.zip'))
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; \
    Parameters: "-ExecutionPolicy Bypass -Command \"& '{app}\\python\\embedded\\python.exe' '{app}\\python\\get-pip.py'\""; \
    Tasks: installpython; Check: FileExists(ExpandConstant('{app}\\python\\get-pip.py'))
=======
    Tasks: installpython
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; \
    Parameters: "-ExecutionPolicy Bypass -Command \"& '{app}\\python\\embedded\\python.exe' '{app}\\python\\get-pip.py'\""; \
    Tasks: installpython
>>>>>> main

; Install Python packages into embedded Python
Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; \
    Parameters: "-ExecutionPolicy Bypass -Command \"& '{app}\\python\\embedded\\python.exe' -m pip install -r '{app}\\requirements.txt'\""; \
<<<<<< codex/design-ultra-powerful-memory-analysis-tool-kadqva
    Tasks: installpackages; Check: FileExists(ExpandConstant('{app}\\python\\embedded\\python.exe'))
=======
    Tasks: installpackages
>>>>>> main

; Enable test signing
Filename: "{sys}\bcdedit.exe"; Parameters: "/set testsigning on"; Tasks: enabletestsigning

; Load driver (optional)
<<<<<< codex/design-ultra-powerful-memory-analysis-tool-kadqva
Filename: "{sys}\sc.exe"; Parameters: "create TitanRW type= kernel start= demand binPath= '{app}\\kernel_driver\\TitanRAM.sys'"; Tasks: installkernel; Check: FileExists(ExpandConstant('{app}\\kernel_driver\\TitanRAM.sys'))
Filename: "{sys}\sc.exe"; Parameters: "start TitanRW"; Tasks: installkernel; Check: FileExists(ExpandConstant('{app}\\kernel_driver\\TitanRAM.sys'))
=======
Filename: "{sys}\sc.exe"; Parameters: "create TitanRW type= kernel start= demand binPath= '{app}\\kernel_driver\\TitanRAM.sys'"; Tasks: installkernel
Filename: "{sys}\sc.exe"; Parameters: "start TitanRW"; Tasks: installkernel
>>>>>> main

[UninstallRun]
Filename: "{sys}\sc.exe"; Parameters: "stop TitanRW"; Flags: runhidden
Filename: "{sys}\sc.exe"; Parameters: "delete TitanRW"; Flags: runhidden

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\\Turkish.isl"
