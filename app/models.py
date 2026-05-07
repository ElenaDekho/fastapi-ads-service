from sqlalchemy import Column, Integer, String, Float, DateTime, func
from database import Base

class Advertisement(Base):
    __tablename__ = "advertisements"        # Имя таблицы в БД

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    author = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Авто-дата создания

    def to_dict(self):
        """Преобразует ответ модели в словарь для ответа API"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "author": self.author,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }