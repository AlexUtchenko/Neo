import mmh3

class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        # Перетворюємо будь-який вхідний тип на рядок для стабільного хешування
        item_str = str(item)
        for i in range(self.num_hashes):
            # mmh3.hash повертає ціле число. 
            # Використовуємо 'i' як seed, щоб отримати різні хеші.
            index = mmh3.hash(item_str, i) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        item_str = str(item)
        for i in range(self.num_hashes):
            index = mmh3.hash(item_str, i) % self.size
            if self.bit_array[index] == 0:
                return False
        return True

def check_password_uniqueness(bloom_filter, passwords):
    """
    Перевірка списку паролів та обробка некоректних даних.
    """
    results = {}
    
    for password in passwords:
        # 1. Валідація даних: перевіряємо, чи пароль є рядком і чи він не порожній
        if password is None:
            results[password] = "некоректні дані (None)"
            continue
            
        # Перевіряємо, чи пароль - рядок, якщо ні, то пробуємо конвертувати його в рядок
        if not isinstance(password, str):
            status_key = str(password) # Щоб використати як ключ у результатах
            results[status_key] = "некоректний тип даних"
            continue

        if not password.strip():
            results[password] = "порожній пароль"
            continue

        # 2. Перевірка через фільтр Блума
        if bloom_filter.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            
    return results

if __name__ == "__main__":
    # Ініціалізація фільтра Блума (розмір 1000 біт, 3 хеш-функції)
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    print("Додаємо існуючі паролі в базу...")
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів (включаючи некоректні випадки для тесту)
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "", None, 12345]
    
    print(f"\nПеревіряємо список: {new_passwords_to_check}\n")
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    print("--- Результати перевірки ---")
    for password, status in results.items():
        display_pass = f"'{password}'" if password is not None else "None"
        print(f"Пароль {display_pass} — {status}.")

