# Create venv and install OCR dependencies under source/
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Source = Join-Path $Root "source"
$Venv = Join-Path $Source ".venv"

if (-not (Test-Path $Venv)) {
    python -m venv $Venv
}
$Py = Join-Path $Venv "Scripts\python.exe"
& $Py -m pip install --upgrade pip
& $Py -m pip install -r (Join-Path $Source "requirements.txt")
Write-Host "Done. Activate: $($Venv)\Scripts\Activate.ps1"
Write-Host "Check OCR: & `"$(Join-Path $Venv 'Scripts\rapidocr.exe')`" check"
