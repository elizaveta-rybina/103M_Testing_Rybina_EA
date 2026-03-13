"""
Модуль для решения квадратных уравнений.
"""
from typing import List, Optional, Union
import math


def solve_quadratic_equation(a: Union[int, float], b: Union[int, float], c: Union[int, float]) -> Optional[List[float]]:
    """
    Находит корни уравнения ax^2 + bx + c = 0 и возвращает их в порядке возрастания.
    
    Args:
        a: Коэффициент при x^2
        b: Коэффициент при x
        c: Свободный член
        
    Returns:
        None, если бесконечное множество решений.
        Список корней (пустой, один элемент или два элемента в порядке возрастания).
    """
    if a == 0:
        if b == 0:
            if c == 0:
                return None  # Бесконечное множество решений (тождество 0 = 0)
            else:
                return []   # Нет решений (неверное равенство, например, 5 = 0)
        else:
            # Линейное уравнение bx + c = 0 -> x = -c / b
            return [-c / b]
            
    # Квадратное уравнение ax^2 + bx + c = 0
    discriminant = b**2 - 4*a*c
    
    if discriminant < 0:
        return []  # Нет действительных корней
    elif discriminant == 0:
        return [-b / (2*a)]  # Один корень
    else:
        root1 = (-b - math.sqrt(discriminant)) / (2*a)
        root2 = (-b + math.sqrt(discriminant)) / (2*a)
        return sorted([root1, root2])  # Два различных корня в порядке возрастания
