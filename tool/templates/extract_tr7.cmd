@echo off
REM TR7-style extract; PowerShell script in same scripts\ folder.
setlocal
if "%~1"=="" (
    echo Usage: extract_tr7.cmd "path\to\screenshot.png"
    echo Paths relative to bundle root work, e.g. demo.png next to verify_image_text.exe
    exit /b 1
)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0chain_extract_tr7.ps1" -ImagePath "%~1"
exit /b %ERRORLEVEL%
