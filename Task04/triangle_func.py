"""
Модуль для определения типа треугольника по функциональному подходу.
"""
from typing import Literal, Union


class IncorrectTriangleSides(Exception):
    """Исключение для некорректных сторон треугольника."""
    pass


def get_triangle_type(a: Union[int, float], b: Union[int, float], c: Union[int, float]) -> Literal["equilateral", "isosceles", "nonequilateral"]:
    """
    Возвращает тип треугольника по длинам его сторон.

    Args:
        a: Первая сторона треугольника
        b: Вторая сторона треугольника
        c: Третья сторона треугольника

    Returns:
        Тип треугольника: 'equilateral', 'isosceles' или 'nonequilateral'

    Raises:
        IncorrectTriangleSides: Если стороны некорректны

    Positives tests:
    >>> get_triangle_type(3, 3, 3)
    'equilateral'
    >>> get_triangle_type(3, 4, 5)
    'nonequilateral'
    >>> get_triangle_type(3, 3, 4)
    'isosceles'

    Negative tests:
    >>> get_triangle_type(1, 2, 3)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    IncorrectTriangleSides: Стороны не образуют треугольник (нарушено неравенство)
    >>> get_triangle_type(-1, 2, 2)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    IncorrectTriangleSides: Длины сторон должны быть положительными числами
    """
    
    if not all(isinstance(side, (int, float)) for side in (a, b, c)):
        raise IncorrectTriangleSides("Стороны должны быть числами")
    
    if a <= 0 or b <= 0 or c <= 0:
        raise IncorrectTriangleSides("Длины сторон должны быть положительными числами")
        
    if a + b <= c or a + c <= b or b + c <= a:
        raise IncorrectTriangleSides("Стороны не образуют треугольник (нарушено неравенство)")

    if a == b == c:
        return "equilateral"
    elif a == b or b == c or a == c:
        return "isosceles"
    else:
        return "nonequilateral"


if __name__ == "__main__":
    import doctest
    
    # Запуск тестов doctest
    doctest.testmod(verbose=True)