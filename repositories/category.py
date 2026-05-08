from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.category import CategoryORM


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_category(self) -> list[CategoryORM]:
        return list(self.db.scalars(select(CategoryORM)).all())

    def get_id_category(self, category_id: str) -> Optional[CategoryORM]:
        return self.db.get(CategoryORM, category_id)

    def create_category(self, name: str) -> CategoryORM:
        new_category = CategoryORM(name=name)
        self.db.add(new_category)
        return new_category

    def delete_category(self, category: CategoryORM) -> None:
        self.db.delete(category)
