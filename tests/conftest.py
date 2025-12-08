import pytest
from unittest.mock import Mock
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


@pytest.fixture
def sample_burger():
    """Фикстура для создания тестового бургера"""
    from praktikum.burger import Burger
    return Burger()

@pytest.fixture(scope='function')
def mock_bun():
    bun = Mock()
    bun.get_name.return_value = "test_bun"
    bun.get_price.return_value = 50
    return bun

@pytest.fixture(scope='function')
def mock_ingredients():
    ingredients = []
    for i in range(3):
        ingredient = Mock()
        ingredient.get_name.return_value = f"ingredient_{i}"
        ingredient.get_type.return_value = INGREDIENT_TYPE_SAUCE if i % 2 == 0 else INGREDIENT_TYPE_FILLING
        ingredient.get_price.return_value = float((i + 1) * 10)
        ingredients.append(ingredient)
    return ingredients

@pytest.fixture(params=[0, 1, 3, 5])
def ingredient_count(request):
    return request.param