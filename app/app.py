from typing import Annotated, Optional
from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
import models
import schemas
from dependencies import get_db_session
from lifespan import lifespan
from services import add_item, get_item, update_item, delete_item, search_items

app = FastAPI(
    title="Ads Service",
    description="Service for buying/selling ads",
    version="0.0.1",
    lifespan=lifespan,      # Создаёт таблицы БД при старте
)

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]

@app.post("/advertisement", response_model=schemas.CreateAdResponse, summary="Создать объявление")
async def create_ad(
    ad_data: schemas.CreateAdRequest,
    session: SessionDep
):
    """Создать объявление"""
    new_ad = await add_item(session, models.Advertisement, ad_data)
    return schemas.CreateAdResponse(id=new_ad.id)

@app.get("/advertisement/{item_id}", response_model=schemas.GetAdResponse, summary="Получить объявление по ID")
async def get_ad(
    item_id: int,
    session: SessionDep
):
    """Получить объявление по ID"""
    ad = await get_item(session, models.Advertisement, item_id)
    return schemas.GetAdResponse(**ad.to_dict())

@app.patch("/advertisement/{item_id}", response_model=schemas.UpdateAdResponse, summary="Обновить объявление")
async def update_ad(
    item_id: int,
    update_data: schemas.UpdateAdRequest,
    session: SessionDep
):
    """Обновить объявление"""
    updated_ad = await update_item(session, models.Advertisement, item_id, update_data)
    return schemas.UpdateAdResponse(**updated_ad.to_dict())

@app.delete("/advertisement/{item_id}", response_model=schemas.OKResponse, summary="Удалить объявление")
async def delete_ad(
    item_id: int,
    session: SessionDep
):
    """Удалить объявление"""
    await delete_item(session, models.Advertisement, item_id)
    return schemas.OKResponse()

@app.get("/advertisement", response_model=list[schemas.GetAdResponse], summary="Поиск объявлений")
async def search_ads(
    session: SessionDep,
    title: Optional[str] = Query(None),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    author: Optional[str] = Query(None)
):
    """Поиск объявлений по фильтрам"""
    ads = await search_items(session, models.Advertisement, title, price_min, price_max, author)
    return [schemas.GetAdResponse(**ad.to_dict()) for ad in ads]