@echo off
REM Adds AIAssistant.exe to Windows auto-start (no admin needed for HKCU)

set "EXE=%~dp0dist\AIAssistant.exe"

if not exist "%EXE%" (
    echo [ERROR] dist\AIAssistant.exe not found. Run build_windows.bat first.
    pause & exit /b 1
)

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" ^
    /v "AIAssistant" /t REG_SZ /d "%EXE%" /f

echo  AI Assistant will auto-start with Windows.
echo    Path: %EXE%
pause
