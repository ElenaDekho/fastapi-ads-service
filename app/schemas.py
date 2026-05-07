from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

# Схема для создания объявления (входные данные)
class CreateAdRequest(BaseModel):
    title: str = Field(..., min_length=1, description="Заголовок объявления")
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="Цена должна быть больше 0")
    author: str = Field(..., min_length=1, description="Автор объявления")

    @field_validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Цена должна быть больше 0')
        return v

# Схема ответа при создании (только ID)
class CreateAdResponse(BaseModel):
    id: int

# Схема полного ответа (для GET и поиска)
class GetAdResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    author: str
    created_at: Optional[datetime] = None

# Схема для обновления (все поля опциональны)
class UpdateAdRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    author: Optional[str] = Field(None, min_length=1)

# Схема ответа после обновления
class UpdateAdResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    author: str
    created_at: Optional[datetime] = None

# Простой статус - ответ
class OKResponse(BaseModel):
    status: str = "ok"
