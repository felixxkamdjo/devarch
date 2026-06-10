from repositories.category_repository import (
    get_all_categories,
    get_category_by_id,
    create_category
)


def list_categories_service():
    return get_all_categories()


def get_category_service(category_id):
    cat = get_category_by_id(category_id)
    if not cat:
        raise ValueError("Category not found.")
    return cat


def create_category_service(name):
    if not name or not name.strip():
        raise ValueError("Category name is required.")
    return create_category(name.strip())