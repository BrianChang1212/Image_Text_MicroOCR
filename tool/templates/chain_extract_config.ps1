# --extract-config with user JSON. Installed under scripts\ in release bundle.
param(
    [Parameter(Mandatory = $true)]
    [string]$ConfigPath,
    [Parameter(Mandatory = $true)]
    [string]$ImagePath
)

$ErrorActionPreference = "Stop"
$BundleRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$Exe = Join-Path $BundleRoot "verify_image_text.exe"
if (-not (Test-Path $Exe)) {
    Write-Error "Missing verify_image_text.exe in bundle root: $Exe"
}

if (-not [System.IO.Path]::IsPathRooted($ConfigPath)) {
    $cfgFull = [System.IO.Path]::GetFullPath((Join-Path $BundleRoot $ConfigPath))
} else {
    $cfgFull = $ConfigPath
}
if (-not (Test-Path -LiteralPath $cfgFull)) {
    Write-Error "Config not found: $cfgFull"
}
$cfgFull = (Resolve-Path -LiteralPath $cfgFull).Path

if (-not [System.IO.Path]::IsPathRooted($ImagePath)) {
    $imgFull = [System.IO.Path]::GetFullPath((Join-Path $BundleRoot $ImagePath))
} else {
    $imgFull = $ImagePath
}
if (-not (Test-Path -LiteralPath $imgFull)) {
    Write-Error "Image not found: $imgFull"
}
$imgFull = (Resolve-Path -LiteralPath $imgFull).Path

$prevEap = $ErrorActionPreference
$ErrorActionPreference = "Continue"
try {
    $raw = & $Exe @(
        $imgFull,
        '--extract-config',
        $cfgFull
    ) 2>$null
    $code = $LASTEXITCODE
} finally {
    $ErrorActionPreference = $prevEap
}

if ($code -ne 0) {
    Write-Error "Extract failed (exit $code). Output: $raw"
}

Write-Output $raw
