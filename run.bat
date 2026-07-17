@echo off
REM ============================================================
REM  A2Tool v4.0 - Windows Launcher
REM  Ultimate All-in-One Penetration Testing Suite
REM  Author: Ayush Rajdev & Anzar Iqbal
REM ============================================================
title A2Tool v4.0 - Ultimate Pentest Suite
color 0A

echo.
echo  ============================================================
echo       A2Tool v4.0 - Ultimate Penetration Testing Suite
echo       Author: Ayush Rajdev ^& Anzar Iqbal
echo  ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo [INFO] Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Auto-install dependencies
echo [*] Checking dependencies...
python -m pip install -r requirements.txt --quiet --break-system-packages >nul 2>&1
echo [+] Dependencies ready!

REM Run A2Tool
echo [*] Starting A2Tool...
python A2Tool.py
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start A2Tool
    pause
    exit /b 1
)

pause
