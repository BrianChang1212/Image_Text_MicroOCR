@echo off
REM Launcher: lives in scripts\; exe is one level up.
setlocal
set "BUNDLE=%~dp0.."
cd /d "%BUNDLE%"
"%BUNDLE%\verify_image_text.exe" %*
exit /b %ERRORLEVEL%
