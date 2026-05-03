@echo off
REM ═══════════════════════════════════════════════════════════════════════
REM  AI Desktop Assistant — Windows Build Script
REM  100%% FREE  •  100%% LOCAL  •  NO API KEYS  •  NO INTERNET
REM ═══════════════════════════════════════════════════════════════════════

echo.
echo  ╔═══════════════════════════════════════════════════════╗
echo  ║   AI Desktop Assistant  —  Local ^& Free Build Tool   ║
echo  ║   Powered by: Ollama + LlamaIndex + pyttsx3           ║
echo  ╚═══════════════════════════════════════════════════════╝
echo.

REM ── Check Python ──────────────────────────────────────────────────────
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo   Download Python 3.10+ from: https://www.python.org/downloads/
    pause & exit /b 1
)
python --version

REM ── Check Ollama ──────────────────────────────────────────────────────
echo.
echo Checking for Ollama...
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  ┌─────────────────────────────────────────────────────────┐
    echo  │  Ollama not found. Please install it:                   │
    echo  │  https://ollama.com/download                            │
    echo  │                                                         │
    echo  │  After install, run:  ollama pull llama3                │
    echo  │  Then restart this script.                              │
    echo  └─────────────────────────────────────────────────────────┘
    echo.
    echo  Continuing build anyway — install Ollama before running.
) else (
    echo   Ollama found.
    echo.
    echo  Pulling llama3 model (this downloads ~4GB, once only)...
    ollama pull llama3
)

REM ── Install Python deps ───────────────────────────────────────────────
echo.
echo [1/3] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo  PyAudio sometimes needs special install on Windows:
    echo    pip install pipwin
    echo    pipwin install pyaudio
    echo  Then re-run this script.
    pause & exit /b 1
)

REM ── Build EXE ─────────────────────────────────────────────────────────
echo.
echo [2/3] Building AIAssistant.exe...
pyinstaller assistant.spec --clean --noconfirm
if %errorlevel% neq 0 (
    echo [ERROR] Build failed. Check errors above.
    pause & exit /b 1
)

REM ── Done ──────────────────────────────────────────────────────────────
echo.
echo [3/3] Done!
echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║    dist\AIAssistant.exe is ready!                      ║
echo  ║                                                          ║
echo  ║  Before running:                                         ║
echo  ║    1. Start Ollama:   ollama serve                       ║
echo  ║    2. Double-click:   dist\AIAssistant.exe               ║
echo  ║                                                          ║
echo  ║  Hotkeys:                                                ║
echo  ║    Ctrl+Alt+A  — toggle voice listening                  ║
echo  ║    Right-click tray icon — chat / memory / quit          ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.
pause
