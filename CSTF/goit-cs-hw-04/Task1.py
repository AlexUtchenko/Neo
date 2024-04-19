from threading import Thread, RLock
import argparse
import time
from pathlib import Path
import math
from multiprocessing import cpu_count


def search_in_files(keyword, files, results, lock):
    """
    Функція для пошуку ключового слова в наборі файлів.
    """
    found_files = []
    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    if keyword in line:
                        found_files.append(file_path)
                        break
        except Exception as e:
            print(f"Помилка при обробці файлу {file_path}: {e}")
    # Збереження результатів пошуку
    with (
        lock
    ):  # блокування доступу до змінної results за допомогою блоку RLock від інших потоків
        results[keyword] = (
            found_files
            if not results.get(keyword)
            else results.get(keyword) + found_files
        )


def batcher(files, threads):
    """
    Функція для прозподілення  файлів серед потоків.
    """
    number_of_batches = (
        len(files) if len(files) < threads else math.ceil(len(files) / threads)
    )
    batches = []
    while files:
        batches.append(files[:number_of_batches])
        files = files[number_of_batches:]
    return batches


def main(folder_path, keywords):
    # Список файлів у текі
    files = [file for file in folder_path.iterdir() if file.is_file()]
    # Кількість потоків, що використовуються
    num_threads = min(
        cpu_count(), len(files)
    )  # Обмежте кількість потоків, щоб уникнути перевантаження системи і створення зайвих потоків
    # Розділення списку файлів між потоками
    file_batches = batcher(files, num_threads)
    # Створення та запуск потоків
    results = {}
    threads = []
    lock = RLock()
    for keyword in keywords:
        for i in range(num_threads):
            thread = Thread(
                target=search_in_files, args=(keyword, file_batches[i], results, lock)
            )
            threads.append(thread)
            thread.start()
    # Зачекати завершення всіх потоків
    for thread in threads:
        thread.join()
    # Виведення результатів у зручному вигляді з словника результатів за умовами завдання
    print(f"\nРезультати пошуку слів  в файлах в багатопоточному режимі.\n")
    for keyword, found_files in results.items():
        print(f"Результати пошуку для '{keyword}':")
        if not found_files:
            print("Нічого не знайдено.")
        else:
            for file_path in found_files:
                print(file_path)
            print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multithreaded file search.")
    parser.add_argument(
        "folder_path", type=str, help="Path to the folder containing files."
    )
    parser.add_argument("keywords", nargs="+", type=str, help="Keywords to search.")
    args = parser.parse_args()

    try:
        path = Path(args.folder_path)
        start_time = time.time()
        main(path, args.keywords)
        end_time = time.time()
        print(f"\nЧас виконання: {end_time - start_time} секунд\n")
    except Exception:
        print("Неправильний шлях до теки.")
