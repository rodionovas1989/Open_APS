from fastapi import FastAPI
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
