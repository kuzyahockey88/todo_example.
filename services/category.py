from sqlalchemy.orm import Session
from repositories.category import CategoryRepository
from schemas.category import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema


class CategoryNotFound(Exception):
    """Задача не найдена в БД"""

class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_category(self) -> list[CategorySchema]:
        category_orm = self.category_repository.get_all_category()
        return [CategorySchema.model_validate(category) for category in category_orm]

    def create_category(self, category_create: CategoryCreateSchema) -> CategorySchema:
        category_orm = self.category_repository.create_category(name=category_create.name)
        self.db.commit()
        return CategorySchema.model_validate(category_orm)

    def update_category(self, category_id: str, category_update: CategoryUpdateSchema) -> CategorySchema:
        category_for_update = self.category_repository.get_id_category(category_id=category_id)
        if not category_for_update:
            raise CategoryNotFound(f'Задача с id {category_id} не найдена')

        if category_update.name is not None:
            category_for_update.name = category_update.name

        self.db.commit()
        return CategorySchema.model_validate(category_for_update)

    def delete_category(self, category_id: str) :
        category_for_delete = self.category_repository.get_id_category(category_id=category_id)
        if not category_for_delete:
            raise CategoryNotFound(f'Задача с id {category_id} не найдена')

        self.category_repository.delete_category(category_for_delete)
        self.db.commit()
