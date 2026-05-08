from sqlalchemy.orm import Mapped

from models.base import Base


class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]
