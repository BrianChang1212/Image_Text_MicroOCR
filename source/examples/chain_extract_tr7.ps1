# Dev example: venv Python. Release: scripts\extract_tr7.cmd + scripts\chain_extract_tr7.ps1 (bundle root has .exe; see tool/templates).
param(
    [Parameter(Mandatory = $true)]
    [string]$ImagePath
)

$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $PSScriptRoot
$Py = Join-Path $Here ".venv\Scripts\python.exe"
$Script = Join-Path $Here "verify_image_text.py"

if (-not (Test-Path $Py)) {
    Write-Error "Run tool\setup_venv.ps1 first. Missing: $Py"
}

$prevEap = $ErrorActionPreference
$ErrorActionPreference = "Continue"
try {
    $raw = & $Py @(
        $Script,
        $ImagePath,
        '--extract',
        'tr7-monitor'
    ) 2>$null
    $code = $LASTEXITCODE
} finally {
    $ErrorActionPreference = $prevEap
}
if ($code -ne 0) {
    Write-Error "Extract failed (exit $code). Raw: $raw"
}

$j = $raw | ConvertFrom-Json
Write-Host "Temperature (C): $($j.temperature_c)"
Write-Host "Humidity (%):    $($j.humidity_percent)"
# Chain: call your tool here, e.g. & .\my_logger.exe $j.temperature_c $j.humidity_percent
