@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================================
echo Open APS Server - Windows Launcher
echo ============================================================
echo.

REM Переходим в директорию скрипта
cd /d "%~dp0"
set PROJECT_DIR=%CD%

REM Активируем виртуальное окружение (предполагается, что оно в родительской папке)
if exist "..\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call ..\venv\Scripts\activate.bat
    echo Virtual environment activated: %CD%\..\venv
) else (
    echo WARNING: Virtual environment not found in parent directory
    echo Creating new virtual environment...
    cd ..
    python -m venv venv
    call venv\Scripts\activate.bat
    cd aps_project
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Checking dependencies...
pip install pydantic-settings --quiet

echo.
echo ============================================================
echo Starting Open APS Server...
echo ============================================================
echo.
echo Available endpoints:
echo   - Web Interface: http://localhost:8000/
echo   - API Docs:      http://localhost:8000/docs
echo   - Health Check:  http://localhost:8000/api/health
echo.
echo Press CTRL+C to stop the server
echo ============================================================
echo.

REM Запускаем сервер с правильным PYTHONPATH
set PYTHONPATH=%PROJECT_DIR%
python run.py

if errorlevel 1 (
    echo.
    echo ERROR: Server failed to start
    echo Try alternative method:
    echo   set PYTHONPATH=.
    echo   python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
    pause
)
