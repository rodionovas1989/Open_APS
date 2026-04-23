@echo off
REM Запуск Open APS сервера для Windows
REM Использование: START_SERVER.bat

echo ============================================================
echo Open APS Server - Windows Launcher
echo ============================================================
echo.

REM Проверка наличия виртуального окружения
if not exist "..\venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please create it first: python -m venv ..\venv
    pause
    exit /b 1
)

echo Activating virtual environment...
call ..\venv\Scripts\activate.bat

REM Проверка активации
if "%VIRTUAL_ENV%"=="" (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Virtual environment activated: %VIRTUAL_ENV%
echo.

REM Проверка зависимостей
echo Checking dependencies...
python -c "import fastapi, uvicorn, sqlalchemy" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

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

REM Запуск сервера с обработкой ошибок
python run.py
if errorlevel 1 (
    echo.
    echo ERROR: Server failed to start
    echo Try alternative method:
    echo   set PYTHONPATH=.
    echo   python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
    echo.
    pause
)
