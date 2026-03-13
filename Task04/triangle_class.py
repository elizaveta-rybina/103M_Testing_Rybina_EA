"""
Модуль для работы с треугольниками (реализация на основе класса).
"""
from typing import Literal, Union


class IncorrectTriangleSides(Exception):
    """Исключение для некорректных сторон треугольника."""
    pass


class Triangle:
    """
    Класс для представления треугольника.
    
    Attributes:
        a: Первая сторона треугольника
        b: Вторая сторона треугольника
        c: Третья сторона треугольника
    """
    
    def __init__(self, a: Union[int, float], b: Union[int, float], c: Union[int, float]) -> None:
        """
        Инициализирует треугольник с проверкой корректности сторон.
        
        Args:
            a: Первая сторона
            b: Вторая сторона
            c: Третья сторона
            
        Raises:
            IncorrectTriangleSides: Если стороны некорректны
        """
        if not all(isinstance(side, (int, float)) for side in (a, b, c)):
            raise IncorrectTriangleSides("Стороны должны быть числами")
        
        if a <= 0 or b <= 0 or c <= 0:
            raise IncorrectTriangleSides("Длины сторон должны быть положительными числами")
            
        if a + b <= c or a + c <= b or b + c <= a:
            raise IncorrectTriangleSides("Стороны не образуют треугольник (нарушено неравенство)")
        
        self.a: Union[int, float] = a
        self.b: Union[int, float] = b
        self.c: Union[int, float] = c
    
    def perimeter(self) -> Union[int, float]:
        """
        Вычисляет периметр треугольника.
        
        Returns:
            Периметр треугольника
        """
        return self.a + self.b + self.c
    
    def triangle_type(self) -> Literal["equilateral", "isosceles", "nonequilateral"]:
        """
        Определяет тип треугольника по длинам сторон.
        
        Returns:
            Тип треугольника: 'equilateral', 'isosceles' или 'nonequilateral'
        """
        if self.a == self.b == self.c:
            return "equilateral"
        elif self.a == self.b or self.b == self.c or self.a == self.c:
            return "isosceles"
        else:
            return "nonequilateral"
