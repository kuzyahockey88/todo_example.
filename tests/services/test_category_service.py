from unittest.mock import Mock

import pytest

from models.category import CategoryORM
from schemas.category import CategoryCreateSchema, CategorySchema, CategoryUpdateSchema
from services.category import CategoryNotFound, CategoryService


def test_list_category_returns_pydantic_models(
    category_service: CategoryService,
    category_repository_mock: Mock,
):

    category_repository_mock.get_all_category.return_value = [
        CategoryORM(id="category-1", name="Изучить pytest"),
        CategoryORM(id="category-2", name="Написать первый тест"),
    ]

    result = category_service.list_category()

    assert result == [
        CategorySchema(id="category-1", name="Изучить pytest"),
        CategorySchema(id="category-2", name="Написать первый тест"),
    ]


def test_create_category_commits_created_task(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
):
    created_category = CategoryORM(id="category-1", name="Новая задача")
    category_repository_mock.create_category.return_value = created_category

    result = category_service.create_category(CategoryCreateSchema(name="Новая задача"))

    category_repository_mock.create_category.assert_called_once_with(
        name="Новая задача"
    )
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "category-1",
        "name": "Новая задача",
    }


@pytest.mark.parametrize(
    ("payload", "expected_name"),
    [
        pytest.param(
            CategoryUpdateSchema(name="Обновить заголовок"),
            "Обновить заголовок",
        ),
    ],
)
def test_update_category_updates_only_passed_fields(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
    payload: CategoryUpdateSchema,
    expected_name: str,
):
    category = CategoryORM(id="category-1", name="Старая задача")
    category_repository_mock.get_id_category.return_value = category

    result = category_service.update_category("category-1", payload)

    category_repository_mock.get_id_category.assert_called_once_with(
        category_id="category-1"
    )
    db_mock.commit.assert_called_once_with()

    assert isinstance(result, CategorySchema)
    assert result.model_dump() == {
        "id": "category-1",
        "name": expected_name,
    }


def test_update_category_raises_when_task_not_found(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get_id_category.return_value = None

    with pytest.raises(CategoryNotFound):
        category_service.update_category(
            "missing-category", CategoryUpdateSchema(name="Неважно")
        )

    db_mock.commit.assert_not_called()
