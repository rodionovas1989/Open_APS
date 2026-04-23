from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from src.database.connection import init_db, close_db
from api.routes import materials

app = FastAPI(
    title="TALARIX APS X5",
    description="Advanced Planning and Scheduling System",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Инициализация базы данных при запуске"""
    print("Initializing database...")
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    """Закрытие подключения к БД при остановке"""
    print("Closing database connections...")
    await close_db()

@app.get("/")
async def root():
    """Главная страница - веб-интерфейс"""
    web_path = os.path.join(os.path.dirname(__file__), "..", "web", "templates", "index.html")
    if os.path.exists(web_path):
        return FileResponse(web_path)
    return {"message": "Welcome to TALARIX APS X5 API", "docs": "/docs"}

# Подключение статических файлов (CSS, JS)
web_static_path = os.path.join(os.path.dirname(__file__), "..", "web", "static")
if os.path.exists(web_static_path):
    app.mount("/static", StaticFiles(directory=web_static_path), name="static")

# Подключение роутов
app.include_router(materials.router, prefix="/api")

# Пример эндпоинта для проверки работоспособности
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "TALARIX APS X5"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
