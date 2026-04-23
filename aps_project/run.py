r"""
Точка входа для запуска APS сервера
Запуск: python run.py

Для Windows PowerShell:
1. cd C:\Users\Talarix\Documents\GitHub\Open_APS\aps_project
2. ..\venv\Scripts\Activate.ps1
3. python run.py
"""

import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print("=" * 60)
print("Open APS Server Starting...")
print("=" * 60)
print(f"Working directory: {os.getcwd()}")
print(f"Python executable: {sys.executable}")
print(f"Python path (first 3): {sys.path[:3]}")
print("=" * 60)

# Проверяем доступность модулей
try:
    from api.main import app
    print("✓ Successfully imported api.main")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("\nSolution:")
    print("1. Make sure you're running from aps_project directory")
    print("2. Make sure virtual environment is activated")
    print("3. Try: $env:PYTHONPATH='.'; python run.py")
    sys.exit(1)

import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Uvicorn server on http://0.0.0.0:8000")
    print("=" * 60)
    print("\nAvailable endpoints:")
    print("  - Web Interface: http://localhost:8000/")
    print("  - API Docs:      http://localhost:8000/docs")
    print("  - Health Check:  http://localhost:8000/api/health")
    print("=" * 60)
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        "api.main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )
