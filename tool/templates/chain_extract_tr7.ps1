# TR7-style screenshot: temperature / humidity JSON. Installed under scripts\ in release bundle.
param(
    [Parameter(Mandatory = $true)]
    [string]$ImagePath
)

$ErrorActionPreference = "Stop"
$BundleRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$Exe = Join-Path $BundleRoot "verify_image_text.exe"
if (-not (Test-Path $Exe)) {
    Write-Error "Missing verify_image_text.exe in bundle root: $Exe"
}

if (-not [System.IO.Path]::IsPathRooted($ImagePath)) {
    $imgFull = [System.IO.Path]::GetFullPath((Join-Path $BundleRoot $ImagePath))
} else {
    $imgFull = $ImagePath
}
if (-not (Test-Path -LiteralPath $imgFull)) {
    Write-Error "Image not found: $imgFull"
}

$prevEap = $ErrorActionPreference
$ErrorActionPreference = "Continue"
try {
    $raw = & $Exe @(
        $imgFull,
        '--extract',
        'tr7-monitor'
    ) 2>$null
    $code = $LASTEXITCODE
} finally {
    $ErrorActionPreference = $prevEap
}
if ($code -ne 0) {
    Write-Error "Extract failed (exit $code). Output: $raw"
}

$j = $raw | ConvertFrom-Json
Write-Host "Temperature (C): $($j.temperature_c)"
Write-Host "Humidity (%):    $($j.humidity_percent)"
if ($j.timestamp) {
    Write-Host "Timestamp:       $($j.timestamp)"
}
