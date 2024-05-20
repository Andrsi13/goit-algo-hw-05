import timeit
import os


# Функція для пошуку підрядка алгоритмом Боєра-Мура
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



# Функція для пошуку підрядка алгоритмом Кнута-Морріса-Пратта
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


def kmp(text, pattern):
    M = len(pattern)
    N = len(text)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено



# Функція для пошуку підрядка алгоритмом Рабіна-Карпа
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



def rabin_karp(text, pattern):
        # Довжини основного рядка та підрядка пошуку
    substring_length = len(pattern)
    main_string_length = len(text)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(pattern, base, modulus)
    current_slice_hash = polynomial_hash(text[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if text[i:i+substring_length] == pattern:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(text[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(text[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1



# шлях до поточної директорії
current_directory = os.path.dirname(__file__)

# Зчитуємо вміст текстових файлів
with open(os.path.join(current_directory, 'text1.txt'), 'r', encoding='utf-8') as file:
    text1 = file.read()
with open(os.path.join(current_directory, 'text2.txt'), 'r', encoding='utf-8') as file:
    text2 = file.read()

# Для статті 1
# Приклади підрядків
existing_pattern_for_text_1 = "як влаштовані алгоритми"
fake_pattern_for_text_1 = "просто рандомний рядрк"


# Вимірюємо час для алгоритму Боєра-Мура
time_bm_existing = timeit.timeit(lambda: boyer_moore_search(text1, existing_pattern_for_text_1), number=1000)
time_bm_fake = timeit.timeit(lambda: boyer_moore_search(text1, fake_pattern_for_text_1), number=1000)

# Вимірюємо час для алгоритму Кнута-Морріса-Пратта
time_kmp_existing = timeit.timeit(lambda: kmp(text1, existing_pattern_for_text_1), number=1000)
time_kmp_fake = timeit.timeit(lambda: kmp(text1, fake_pattern_for_text_1), number=1000)

# Вимірюємо час для алгоритму Рабіна-Карпа
time_rk_existing = timeit.timeit(lambda: rabin_karp(text1, existing_pattern_for_text_1), number=1000)
time_rk_fake = timeit.timeit(lambda: rabin_karp(text1, fake_pattern_for_text_1), number=1000)

# Для статті 2
# Приклади підрядків

existing_pattern_for_text_2 = "проведено"
fake_pattern_for_text_2 = "просто рандомний рядок"

# Вимірюємо час для алгоритму Боєра-Мура
time_bm_existing_2 = timeit.timeit(lambda: boyer_moore_search(text2, existing_pattern_for_text_2), number=1000)
time_bm_fake_2 = timeit.timeit(lambda: boyer_moore_search(text2, fake_pattern_for_text_2), number=1000)

# Вимірюємо час для алгоритму Кнута-Морріса-Пратта
time_kmp_existing_2 = timeit.timeit(lambda: kmp(text2, existing_pattern_for_text_2), number=1000)
time_kmp_fake_2 = timeit.timeit(lambda: kmp(text2, fake_pattern_for_text_2), number=1000)

# Вимірюємо час для алгоритму Рабіна-Карпа
time_rk_existing_2 = timeit.timeit(lambda: rabin_karp(text2, existing_pattern_for_text_2), number=1000)
time_rk_fake_2 = timeit.timeit(lambda: rabin_karp(text2, fake_pattern_for_text_2), number=1000)

# Виводимо результати
print("Для статті 1:")
print("Час для алгоритму Боєра-Мура (існуючий підрядок):", time_bm_existing)
print("Час для алгоритму Боєра-Мура (вигаданий підрядок):", time_bm_fake)

print("Час для алгоритму Кнута-Морріса-Пратта (існуючий підрядок):", time_kmp_existing)
print("Час для алгоритму Кнута-Морріса-Пратта (вигаданий підрядок):", time_kmp_fake)

print("Час для алгоритму Рабіна-Карпа (існуючий підрядок):", time_rk_existing)
print("Час для алгоритму Рабіна-Карпа (вигаданий підрядок):", time_rk_fake)

# Виводимо результати
print("Для статті 2:")
print("Час для алгоритму Боєра-Мура (існуючий підрядок):", time_bm_existing_2)
print("Час для алгоритму Боєра-Мура (вигаданий підрядок):", time_bm_fake_2)

print("Час для алгоритму Кнута-Морріса-Пратта (існуючий підрядок):", time_kmp_existing_2)
print("Час для алгоритму Кнута-Морріса-Пратта (вигаданий підрядок):", time_kmp_fake_2)

print("Час для алгоритму Рабіна-Карпа (існуючий підрядок):", time_rk_existing_2)
print("Час для алгоритму Рабіна-Карпа (вигаданий підрядок):", time_rk_fake_2)
