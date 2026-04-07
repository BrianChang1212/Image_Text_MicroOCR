@echo off
REM Config (JSON) + image. Relative paths are from bundle root (folder with verify_image_text.exe).
setlocal
if "%~2"=="" (
    echo Usage: extract_with_config.cmd config\your.json "path\to\image.png"
    echo Example: extract_with_config.cmd ..\config\extract_config.example.json "D:\shot.png"
    exit /b 1
)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0chain_extract_config.ps1" -ConfigPath "%~1" -ImagePath "%~2"
exit /b %ERRORLEVEL%
