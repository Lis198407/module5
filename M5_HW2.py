"""
Вимоги до завдання:
Функція generator_numbers(text: str) повинна приймати рядок як аргумент і повертати генератор, що ітерує по всіх дійсних числах у тексті. 
Дійсні числа у тексті вважаються записаними без помилок і чітко відокремлені пробілами з обох боків.
Функція sum_profit(text: str, func: Callable) має використовувати генератор generator_numbers для обчислення загальної суми чисел 
        у вхідному рядку та приймати його як аргумент при виклику.

Рекомендації для виконання:
Використовуйте регулярні вирази для ідентифікації дійсних чисел у тексті, з урахуванням, що числа чітко відокремлені пробілами.
Застосуйте конструкцію yield у функції generator_numbers для створення генератора.
Переконайтеся, що sum_profit коректно обробляє дані від generator_numbers і підсумовує всі числа.

Критерії оцінювання:
Правильність визначення та повернення дійсних чисел функцією generator_numbers.
Коректність обчислення загальної суми в sum_profit.
Чистота коду, наявність коментарів та відповідність стилю кодування PEP8.
"""
from typing import Callable

def generator_numbers(text: str):
    pass

def sum_profit(text: str, func: Callable):
    pass

def main():
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")

if __name__ == "__main__":
    main()
