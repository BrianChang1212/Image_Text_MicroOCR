# Mirror PyInstaller onedir output into release\verify_image_text (no full delete; works if folder is in use).
$ErrorActionPreference = "Stop"
$ReleaseRoot = $PSScriptRoot
$ProjectRoot = Split-Path -Parent $ReleaseRoot
$DevDist = Join-Path $ProjectRoot "source\dist\verify_image_text"
$Target = Join-Path $ReleaseRoot "verify_image_text"

$DevDist = [System.IO.Path]::GetFullPath($DevDist)

if (-not (Test-Path (Join-Path $DevDist "verify_image_text.exe"))) {
    Write-Error "Missing build output: $DevDist\verify_image_text.exe. Run tool\build_pyinstaller_release.ps1 first."
}

Write-Host "Mirroring from: $DevDist" -ForegroundColor Cyan
Write-Host "            to: $Target" -ForegroundColor Cyan
New-Item -ItemType Directory -Path $Target -Force | Out-Null

# Robocopy: 0-7 = success; >=8 = failure. /MIR = sync + remove extras in dest.
& robocopy.exe $DevDist $Target /MIR /R:2 /W:2 /NFL /NDL /NJH /NJS /NC /NS /NP
$rc = $LASTEXITCODE
if ($rc -ge 8) {
    Write-Error "robocopy failed with exit code $rc"
}
Write-Host "Done (robocopy exit $rc)." -ForegroundColor Green
