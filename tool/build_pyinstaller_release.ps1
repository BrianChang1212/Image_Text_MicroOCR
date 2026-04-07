# Build a Windows folder distribution (no Python needed on target PCs).
# Prerequisite: run setup_venv.ps1 once so source\.venv exists.
param(
    [switch]$SyncToRelease
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Source = Join-Path $Root "source"
$Py = Join-Path $Source ".venv\Scripts\python.exe"
$Templates = Join-Path $PSScriptRoot "templates"

if (-not (Test-Path $Py)) {
    Write-Error "Missing $Py. Run tool\setup_venv.ps1 first."
}

Push-Location $Source
try {
    & $Py -m pip install -r (Join-Path $Source "requirements-build.txt")

    $distDir = Join-Path $Source "dist\verify_image_text"
    if (Test-Path $distDir) {
        Remove-Item -Recurse -Force $distDir
    }

    # Note: Avoid --collect-all onnxruntime (pulls huge optional transformer tooling).
    # PyInstaller's hook-onnxruntime collects the native runtime DLLs.
    & $Py -m PyInstaller --noconfirm --clean --onedir `
        --name verify_image_text `
        --collect-all rapidocr `
        verify_image_text.py

    $scriptsDir = Join-Path $distDir "scripts"
    $configDir = Join-Path $distDir "config"
    $docDir = Join-Path $distDir "doc"
    New-Item -ItemType Directory -Force -Path $scriptsDir, $configDir, $docDir | Out-Null

    Copy-Item (Join-Path $Templates "run_ocr.bat") -Destination $scriptsDir -Force
    Copy-Item (Join-Path $Templates "ocr_plain.bat") -Destination $scriptsDir -Force
    Copy-Item (Join-Path $Templates "chain_extract_tr7.ps1") -Destination $scriptsDir -Force
    Copy-Item (Join-Path $Templates "extract_tr7.cmd") -Destination $scriptsDir -Force
    Copy-Item (Join-Path $Templates "chain_extract_config.ps1") -Destination $scriptsDir -Force
    Copy-Item (Join-Path $Templates "extract_with_config.cmd") -Destination $scriptsDir -Force
    Copy-Item (Join-Path $Templates "extract_config.example.json") -Destination $configDir -Force
    Copy-Item (Join-Path $Templates "OCR_README_FOR_USERS.txt") -Destination $docDir -Force
    Copy-Item (Join-Path $Templates "release_bundle_README.txt") -Destination (Join-Path $distDir "README.txt") -Force

    Write-Host ""
    Write-Host "Build output: $distDir" -ForegroundColor Green
    Write-Host "Zip the folder 'verify_image_text' (entire directory) for distribution." -ForegroundColor Cyan

    if ($SyncToRelease) {
        $SyncScript = Join-Path $Root "release\sync_from_dev_build.ps1"
        if (-not (Test-Path $SyncScript)) {
            Write-Warning "Release sync script not found: $SyncScript"
        } else {
            Write-Host "Syncing to release\ ..." -ForegroundColor Cyan
            & $SyncScript
        }
    }
}
finally {
    Pop-Location
}
