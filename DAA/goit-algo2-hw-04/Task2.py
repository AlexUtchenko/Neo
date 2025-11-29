from typing import List

# Копіюємо клас Trie з теорії
class TrieNode:
    def __init__(self):
        self.children = {}
        self.value = None

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.size = 0

    def put(self, key, value=None):
        if not isinstance(key, str) or not key:
            raise TypeError(f"Illegal argument for put: key = {key} must be a non-empty string")

        current = self.root
        for char in key:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        if current.value is None:
            self.size += 1
        current.value = value

    def get(self, key):
        if not isinstance(key, str) or not key:
            raise TypeError(f"Illegal argument for get: key = {key} must be a non-empty string")

        current = self.root
        for char in key:
            if char not in current.children:
                return None
            current = current.children[char]
        return current.value

    def delete(self, key):
        if not isinstance(key, str) or not key:
            raise TypeError(f"Illegal argument for delete: key = {key} must be a non-empty string")

        def _delete(node, key, depth):
            if depth == len(key):
                if node.value is not None:
                    node.value = None
                    self.size -= 1
                    return len(node.children) == 0
                return False

            char = key[depth]
            if char in node.children:
                should_delete = _delete(node.children[char], key, depth + 1)
                if should_delete:
                    del node.children[char]
                    return len(node.children) == 0 and node.value is None
            return False

        return _delete(self.root, key, 0)

    def is_empty(self):
        return self.size == 0

    def longest_prefix_of(self, s):
        if not isinstance(s, str) or not s:
            raise TypeError(f"Illegal argument for longestPrefixOf: s = {s} must be a non-empty string")

        current = self.root
        longest_prefix = ""
        current_prefix = ""
        for char in s:
            if char in current.children:
                current = current.children[char]
                current_prefix += char
                if current.value is not None:
                    longest_prefix = current_prefix
            else:
                break
        return longest_prefix

    def keys_with_prefix(self, prefix):
        if not isinstance(prefix, str):
            raise TypeError(f"Illegal argument for keysWithPrefix: prefix = {prefix} must be a string")

        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]

        result = []
        self._collect(current, list(prefix), result)
        return result

    def _collect(self, node, path, result):
        if node.value is not None:
            result.append("".join(path))
        for char, next_node in node.children.items():
            path.append(char)
            self._collect(next_node, path, result)
            path.pop()

    def keys(self):
        result = []
        self._collect(self.root, [], result)
        return result

# Починаємо робити ДЗ

class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        """
        Повертає кількість слів у дереві, які закінчуються на pattern.
        """
        if not isinstance(pattern, str):
            raise TypeError(f"Pattern must be a string, got {type(pattern)}")

        # Використовуємо вже існуючий метод батьківського класу для отримання всіх слів
        all_words = self.keys()
        
        count = 0
        for word in all_words:
            if word.endswith(pattern):
                count += 1
        
        return count

    def has_prefix(self, prefix) -> bool:
        """
        Повертає True, якщо в дереві є хоча б одне слово, що починається на prefix.
        """
        if not isinstance(prefix, str):
            raise TypeError(f"Prefix must be a string, got {type(prefix)}")

        current = self.root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
            
        # Якщо цикл пройшов до кінця, значить шлях у графі існує
        return True

if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat
    
    # Додаткові перевірки
    print(f"Suffix 'apple': {trie.count_words_with_suffix('apple')}") # має бути 1
    
    # Перевірка обробки помилок
    try:
        trie.has_prefix(10)
    except TypeError as e:
        print(f"Успішно перехоплено помилку: {e}")

    print("Всі тести пройдено успішно!")