import pytest
from unittest.mock import Mock, patch, call
from typing import List

from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING

class TestBurger:
    def test_burger(self):
        burger = Burger()
        assert burger.bun is None
        assert burger.ingredients == []
        assert isinstance(burger.ingredients, list)

    @pytest.mark.parametrize("bun_name, bun_price", [
        ("black bun", 100),
        ("white bun", 200),
        ("red bun", 300),
        ("", 0),
        ("special bun", 999),
    ])
    def test_set_buns(self, bun_name, bun_price): 
        # Arrange
        burger = Burger()
        bun = Mock()
        bun.get_name.return_value = bun_name
        bun.get_price.return_value = bun_price
        
        # Act
        burger.set_buns(bun)
        
        # Assert
        assert burger.bun == bun
        bun.get_name.assert_not_called()
        bun.get_price.assert_not_called()
        
    def test_add_ingredient_single(self):
        """Добавляем один ингредиент"""
        # Arrange
        burger = Burger()
        mock_ingredient = Mock()
        mock_ingredient.get_name.return_value = "hot sauce"
        mock_ingredient.get_price.return_value = 50.0
        mock_ingredient.get_type.return_value = INGREDIENT_TYPE_SAUCE
        
        # Act
        burger.add_ingredient(mock_ingredient)
        
        # Assert
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient
        
    @pytest.mark.parametrize("num_ingredients", [1, 3, 5, 10])
    def test_add_multiple_ingredients(self, num_ingredients):
        """Добавляем нескольких ингредиентов"""
        # Arrange
        burger = Burger()
        mock_ingredients = []
        
        for i in range(num_ingredients):
            mock_ingredient = Mock(spec=Ingredient)
            mock_ingredient.get_name.return_value = f"Ingredient {i}"
            mock_ingredient.get_price.return_value = float(i * 10)
            mock_ingredient.get_type.return_value = INGREDIENT_TYPE_SAUCE if i % 2 == 0 else INGREDIENT_TYPE_FILLING
            mock_ingredients.append(mock_ingredient)
        
        # Act
        for ingredient in mock_ingredients:
            burger.add_ingredient(ingredient)
        
        # Assert
        assert len(burger.ingredients) == num_ingredients
        assert burger.ingredients == mock_ingredients
    
    def test_remove_ingredient_by_index(self):
        """Удаляем ингредиент по индексу"""
        # Arrange
        burger = Burger()
        mock_ingredients = [Mock(),Mock(),Mock()]
        for ingredient in mock_ingredients:
            burger.add_ingredient(ingredient)
        
        # Act
        burger.remove_ingredient(1)
        
        # Assert
        assert len(burger.ingredients) == 2
        assert burger.ingredients == [mock_ingredients[0], mock_ingredients[2]]
    
    def test_remove_last_ingredient(self):
        """Удаляем последний ингредиент"""
        # Arrange
        burger = Burger()
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        
        # Act
        burger.remove_ingredient(0)
        
        # Assert
        assert burger.ingredients == []
        
    @pytest.mark.parametrize("index_to_remove", [(-1),(5),(10)])
    def test_remove_ingredient_invalid_index_raises_exception(self, index_to_remove):
        """Удаляем с невалидным индексом"""
        # Arrange
        burger = Burger()
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        
        # Act & Assert
        with pytest.raises(IndexError):
             burger.remove_ingredient(5)  
    
        with pytest.raises(IndexError):
            burger.remove_ingredient(10)

    # Тесты для move_ingredient
    def test_move_ingredient(self):
        """Перемещение ингредиента"""
        # Arrange
        burger = Burger()
        mock_ingredients = [Mock(),Mock(),Mock(),Mock()]
        for ingredient in mock_ingredients:
            burger.add_ingredient(ingredient)
        original_order = burger.ingredients.copy()
        
        # Act
        burger.move_ingredient(1, 3)  # перемещаем второй элемент в конец
        
        # Assert
        assert len(burger.ingredients) == 4
        assert burger.ingredients[0] == original_order[0]
        assert burger.ingredients[1] == original_order[2]
        assert burger.ingredients[2] == original_order[3]
        assert burger.ingredients[3] == original_order[1]
    
    def test_get_price_with_ingredients(self):
        """Цена с булочкой и ингредиентами"""
        # Arrange
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = 30   
        mock_ingredient1 = Mock()
        mock_ingredient1.get_price.return_value = 20       
        mock_ingredient2 = Mock()
        mock_ingredient2.get_price.return_value = 15      
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        
        # Act
        price = burger.get_price()
        
        # Assert
        assert mock_bun.get_price.call_count == 1
        mock_ingredient1.get_price.assert_called_once()
        mock_ingredient2.get_price.assert_called_once()
        assert price == 95  # (30 * 2) + 20 + 15

    @pytest.mark.parametrize("bun_price, ingredient_prices, expected_total", [
        (100, [], 200),  # только булочка
        (50, [10], 110),  # булочка + 1 ингредиент
        (30, [20, 15, 25], 120),  # булочка + 3 ингредиента
        (0, [0, 0], 0),  # нулевые цены
        (25.5, [10.1, 20.2, 30.3], 111.6),  # дробные цены
    ])
    def test_get_price_parameterized(self, bun_price, ingredient_prices, expected_total):
        """Расчет цены"""
        # Arrange
        burger = Burger()     
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        mock_ingredients = []
        for i, ingredient_price in enumerate(ingredient_prices):
            mock_ingredient = Mock()
            mock_ingredient.get_price.return_value = ingredient_price
            mock_ingredients.append(mock_ingredient)     
        burger.set_buns(mock_bun)
        for ingredient in mock_ingredients:
            burger.add_ingredient(ingredient)
        
        # Act
        price = burger.get_price()
        
        # Assert
        assert price == pytest.approx(expected_total, 0.01)

    def test_get_receipt_only_bun(self):
        """Чек только с булочкой"""
        # Arrange
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_name.return_value = "black bun"
        mock_bun.get_price.return_value = 100
        
        burger.set_buns(mock_bun)
        
        # Act
        receipt = burger.get_receipt()
        
        # Assert
        expected_lines = [
            "(==== black bun ====)",
            "(==== black bun ====)",
            "",
            "Price: 200"
        ]
        assert receipt.split('\n') == expected_lines
        assert mock_bun.get_name.call_count == 2
        assert "black bun" in receipt
        assert "Price: 200" in receipt

    def test_get_receipt_with_ingredients(self):
        """Чек с булочкой и ингредиентами"""
        # Arrange
        burger = Burger()
        
        mock_bun = Mock()
        mock_bun.get_name.return_value = "white bun"
        mock_bun.get_price.return_value = 50
        
        mock_sauce = Mock()
        mock_sauce.get_name.return_value = "hot sauce"
        mock_sauce.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock_sauce.get_price.return_value = 30
        
        mock_filling = Mock()
        mock_filling.get_name.return_value = "cutlet"
        mock_filling.get_type.return_value = INGREDIENT_TYPE_FILLING
        mock_filling.get_price.return_value = 70
        
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_sauce)
        burger.add_ingredient(mock_filling)
        
        # Act
        receipt = burger.get_receipt()
        
        # Assert
        expected_lines = [
            "(==== white bun ====)",
            "= sauce hot sauce =",
            "= filling cutlet =",
            "(==== white bun ====)",
            "",
            "Price: 200"
        ]
        assert receipt.split('\n') == expected_lines
        assert mock_bun.get_name.call_count == 2
        mock_sauce.get_name.assert_called_once()
        mock_sauce.get_type.assert_called_once()
        mock_filling.get_name.assert_called_once()
        mock_filling.get_type.assert_called_once()