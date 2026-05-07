# app/services.py
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import models, schemas


async def add_item(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_data: schemas.CreateAdRequest
) -> models.Advertisement:
    new_item = orm_model(**item_data.model_dump())
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item


async def get_item(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_id: int
) -> models.Advertisement:
    stmt = select(orm_model).where(orm_model.id == item_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Advertisement with id {item_id} not found"
        )
    return item


async def update_item(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_id: int,
        update_data: schemas.UpdateAdRequest
) -> models.Advertisement:
    item = await get_item(session, orm_model, item_id)
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(item, key, value)

    await session.commit()
    await session.refresh(item)
    return item


async def delete_item(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_id: int
) -> None:
    item = await get_item(session, orm_model, item_id)
    await session.delete(item)
    await session.commit()


async def search_items(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        title: str = None,
        price_min: float = None,
        price_max: float = None,
        author: str = None
) -> list[models.Advertisement]:
    stmt = select(orm_model)

    if title:
        stmt = stmt.where(orm_model.title.ilike(f"%{title}%"))
    if price_min is not None:
        stmt = stmt.where(orm_model.price >= price_min)
    if price_max is not None:
        stmt = stmt.where(orm_model.price <= price_max)
    if author:
        stmt = stmt.where(orm_model.author.ilike(f"%{author}%"))

    result = await session.execute(stmt)
    return result.scalars().all()