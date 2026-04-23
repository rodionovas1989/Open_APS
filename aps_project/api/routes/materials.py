from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import select
from src.models.metadata import Material
from src.database.connection import get_db

router = APIRouter(prefix="/materials", tags=["materials"])

class MaterialCreate(BaseModel):
    name: str
    article: str
    counterparty: Optional[str] = None
    accounting_model: Optional[str] = "FIFO"
    shelf_life: Optional[int] = None

class MaterialResponse(MaterialCreate):
    id: int
    
    class Config:
        from_attributes = True

@router.get("", response_model=List[MaterialResponse])
async def get_materials():
    async with get_db() as session:
        result = await session.execute(select(Material))
        materials = result.scalars().all()
        return materials

@router.get("/{article}", response_model=MaterialResponse)
async def get_material(article: str):
    async with get_db() as session:
        result = await session.execute(select(Material).where(Material.article == article))
        material = result.scalar_one_or_none()
        if not material:
            raise HTTPException(status_code=404, detail="Материал не найден")
        return material

@router.post("", response_model=MaterialResponse)
async def create_material(material: MaterialCreate):
    async with get_db() as session:
        # Проверка на дубликат
        result = await session.execute(select(Material).where(Material.article == material.article))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Материал с таким артикулом уже существует")
        
        db_material = Material(**material.model_dump())
        session.add(db_material)
        await session.commit()
        await session.refresh(db_material)
        return db_material

@router.put("/{article}", response_model=MaterialResponse)
async def update_material(article: str, material: MaterialCreate):
    async with get_db() as session:
        result = await session.execute(select(Material).where(Material.article == article))
        db_material = result.scalar_one_or_none()
        if not db_material:
            raise HTTPException(status_code=404, detail="Материал не найден")
        
        for key, value in material.model_dump().items():
            setattr(db_material, key, value)
        
        await session.commit()
        await session.refresh(db_material)
        return db_material

@router.delete("/{article}")
async def delete_material(article: str):
    async with get_db() as session:
        result = await session.execute(select(Material).where(Material.article == article))
        db_material = result.scalar_one_or_none()
        if not db_material:
            raise HTTPException(status_code=404, detail="Материал не найден")
        
        await session.delete(db_material)
        await session.commit()
        return {"message": "Материал успешно удален"}
