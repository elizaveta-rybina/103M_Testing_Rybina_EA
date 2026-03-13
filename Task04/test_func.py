"""
Модульные тесты для функции get_triangle_type.
"""
import unittest
from triangle_func import get_triangle_type, IncorrectTriangleSides


class TestTriangleFunc(unittest.TestCase):
    """Набор тестов для функции определения типа треугольника."""

    def test_equilateral(self) -> None:
        """Тест для равностороннего треугольника."""
        self.assertEqual(get_triangle_type(5, 5, 5), "equilateral")

    def test_isosceles(self) -> None:
        """Тест для равнобедренного треугольника."""
        self.assertEqual(get_triangle_type(5, 5, 3), "isosceles")
        self.assertEqual(get_triangle_type(3, 5, 5), "isosceles")
        self.assertEqual(get_triangle_type(5, 3, 5), "isosceles")

    def test_nonequilateral(self) -> None:
        """Тест для разностороннего треугольника."""
        self.assertEqual(get_triangle_type(3, 4, 5), "nonequilateral")

    def test_zero_sides(self) -> None:
        """Тест для нулевой длины стороны."""
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(0, 4, 5)

    def test_negative_sides(self) -> None:
        """Тест для отрицательной длины стороны."""
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(3, -4, 5)

    def test_triangle_inequality(self) -> None:
        """Тест для нарушения неравенства треугольника."""
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(1, 2, 3)


if __name__ == '__main__':
    unittest.main()