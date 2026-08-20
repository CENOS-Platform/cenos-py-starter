@echo off
setlocal
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
set "exit_code=%ERRORLEVEL%"
echo.
if not "%exit_code%"=="0" (
  echo Setup did not complete. Review the message above.
  pause
)
exit /b %exit_code%
