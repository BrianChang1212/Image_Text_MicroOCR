@echo off
REM Plain OCR; exe in bundle root.
setlocal
set "BUNDLE=%~dp0.."
cd /d "%BUNDLE%"
"%BUNDLE%\verify_image_text.exe" --plain %*
exit /b %ERRORLEVEL%
