"""
https://www.edu.goit.global/uk/learn/20318415/19951493/19951593/training?blockId=22652027

Вимоги до завдання:
Функція caching_fibonacci() повинна повертати внутрішню функцію fibonacci(n).
fibonacci(n) обчислює n-те число Фібоначчі. Якщо число вже знаходиться у кеші, функція має повертати значення з кешу.
Якщо число не знаходиться у кеші, функція має обчислити його, зберегти у кеш та повернути результат.
Використання рекурсії для обчислення чисел Фібоначчі.

Критерії оцінювання:
Коректність реалізації функції fibonacci(n) з урахуванням використання кешу.
Ефективне використання рекурсії та кешування для оптимізації обчислень.
Чистота коду, включаючи читабельність та наявність коментарів.
"""

def caching_fibonacci():
    cache = {}     # Створити порожній словник cache

    def fibonacci(n):
        if n <= 0: return 0 # Якщо n <= 0, повернути 0
        elif n == 1: return 1 # Якщо n == 1, повернути 1
        else:
            if not n in cache: #перевырка чи э в кеші
                cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
            return cache[n]  # повернути cache
    return fibonacci

def main():
    fib = caching_fibonacci()      # Отримуємо функцію fibonacci
    print(fib(10))

if __name__ == "__main__":
    main()
