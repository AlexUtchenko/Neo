"""
Завдання 3

Порівняти ефективність алгоритмів пошуку підрядка: 
Боєра-Мура, Кнута-Морріса-Пратта та Рабіна-Карпа на основі двох текстових файлів (стаття 1, стаття 2). 
Використовуючи timeit, треба виміряти час виконання кожного алгоритму для двох видів підрядків: 
одного, що дійсно існує в тексті, та іншого — вигаданого (вибір підрядків за вашим бажанням). 
На основі отриманих даних визначити найшвидший алгоритм для кожного тексту окремо та в цілому.

"""

import timeit
import pandas as pd


# алгоритм Боєра-Мура
def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1


# алгоритм Кнута-Морріса-Пратта
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено


# алгоритм Рабін-Карпа
def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


if __name__ == '__main__':

    with open('article1.txt', 'r') as f:
        text1 = f.read()
    
    with open('article2.txt', 'r') as f:
        text2 = f.read()
    
    substring_1_exist = text1[len(text1) // 4 : len(text1) // 4 + 30]
    substring_1_nexist = 'Слава Україні'
    substring_2_exist = text2[len(text2) // 6 : len(text2) // 6 + 120]
    substring_2_nexist = 'Героям Слава'

    methods = {
        'Боєра-Мура': boyer_moore_search,
        'Кнута-Морріса-Пратта': kmp_search,
        'Рабін-Карпа': rabin_karp_search
    }

    cases = {
        'Текст 1 + існує підрядок': (text1, substring_1_exist),
        'Текст 1 + не існує підрядок': (text1, substring_1_nexist),
        'Текст 2 + існує підрядок': (text2, substring_2_exist),
        'Текст 2 + не існує підрядок': (text2, substring_2_nexist), 
    }

t_bm = []
t_kmp = []
t_rk = []

for name, (text, substring) in cases.items():
    t_bm.append(timeit.timeit(lambda: methods['Боєра-Мура'](text, substring), number=30))
    t_kmp.append(timeit.timeit(lambda: methods['Кнута-Морріса-Пратта'](text, substring), number=30))
    t_rk.append(timeit.timeit(lambda: methods['Рабін-Карпа'](text, substring), number=30))

# створюємо таблицю результатів
df = pd.DataFrame({
    'Боєра-Мура': t_bm,
    'Кнута-Морріса-Пратта': t_kmp,
    'Рабін-Карпа': t_rk},
    index=[name for name in cases.keys()])

print(df)
