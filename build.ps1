param(
    [string]$Mode = "pyside6-deploy"
)

$ErrorActionPreference = "Stop"

Write-Host "[TitanRAM] Build mode: $Mode"

function Ensure-Tool {
    param([string]$Tool)
    if (-not (Get-Command $Tool -ErrorAction SilentlyContinue)) {
        throw "Required tool not found: $Tool"
    }
}

if ($Mode -eq "pyside6-deploy") {
    Ensure-Tool "pyside6-deploy"
    pyside6-deploy --mode=onefile --name TitanRAM --force
} elseif ($Mode -eq "pyinstaller") {
    Ensure-Tool "pyinstaller"
    pyinstaller installer/titanram.spec
} else {
    throw "Unknown mode: $Mode"
}

Write-Host "[TitanRAM] Build complete."
