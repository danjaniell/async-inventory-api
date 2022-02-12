from sqlalchemy import Column, String, Integer
from app.data.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)

    def __repr__(self):
        return (
            f"<Item(id={self.id}, "
            f'name="{self.name}", '
            f"description={self.description})>"
        )
