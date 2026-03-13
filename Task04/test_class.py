"""
Тесты для класса Triangle.
"""
import pytest
from triangle_class import Triangle, IncorrectTriangleSides


# Позитивные тесты
def test_triangle_creation_and_perimeter() -> None:
    """Тест создания треугольника и вычисления периметра."""
    t = Triangle(3, 4, 5)
    assert t.perimeter() == 12


def test_triangle_type_equilateral() -> None:
    """Тест определения равностороннего треугольника."""
    t = Triangle(4.5, 4.5, 4.5)
    assert t.triangle_type() == "equilateral"


def test_triangle_type_isosceles() -> None:
    """Тест определения равнобедренного треугольника."""
    t = Triangle(5, 5, 8)
    assert t.triangle_type() == "isosceles"


def test_triangle_type_nonequilateral() -> None:
    """Тест определения разностороннего треугольника."""
    t = Triangle(6, 8, 10)
    assert t.triangle_type() == "nonequilateral"


# Негативные тесты
def test_triangle_creation_zero_side() -> None:
    """Тест создания треугольника с нулевой стороной."""
    with pytest.raises(IncorrectTriangleSides):
        Triangle(0, 5, 5)


def test_triangle_creation_negative_side() -> None:
    """Тест создания треугольника с отрицательной стороной."""
    with pytest.raises(IncorrectTriangleSides):
        Triangle(5, -5, 5)


def test_triangle_creation_invalid_inequality() -> None:
    """Тест создания треугольника с нарушением неравенства."""
    with pytest.raises(IncorrectTriangleSides):
        Triangle(1, 10, 12)


def test_triangle_creation_string_type() -> None:
    """Тест создания треугольника со строковыми параметрами."""
    with pytest.raises(IncorrectTriangleSides):
        Triangle("3", 4, 5)  # type: ignore