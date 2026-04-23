import os
import shutil

# Создаем полную структуру проекта с рабочими файлами
project_dir = "aps_project_fixed"

# Структура файлов
files = {
    "api/__init__.py": "",
    "api/main.py": '''from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from src.database.connection import init_db, close_db

app = FastAPI(
    title="Open APS",
    description="Advanced Planning and Scheduling System",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

@app.get("/")
async def root():
    return {"message": "Welcome to Open APS API", "docs": "/docs"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Open APS"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''',
    "src/__init__.py": "",
    "src/database/__init__.py": "",
    "src/database/connection.py": '''from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./aps_database.db")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
''',
}

for path, content in files.items():
    full_path = os.path.join(project_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(content)

print("Fixed project created in aps_project_fixed/")
