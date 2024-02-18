from pathlib import Path
from collections import defaultdict
import argparse


TRANSFER_DICT = defaultdict(lambda: [])
FOLDERS = []


def get_extensions(file_name) -> str:
    return Path(file_name).suffix[1:].upper()


def scan(folder: Path):
    """Функції сканує рекурсивно директорії в глибину, починаючи від заданої. Вносить перелік файлів за ключем їх розширеня в словник переносу і список тек для видалення"""
    for item in folder.iterdir():
        if item.is_dir():
            FOLDERS.append(item)
            scan(
                item
            )  # рекурсивний виклик функції для заглиблення на рівень нижче в файловій системі
        else:
            # наповнення словника переносу
            extension = get_extensions(item.name)
            new_name = folder / item.name
            if not extension:
                TRANSFER_DICT["NON_EXTENSION"].append(new_name)
            else:
                TRANSFER_DICT[extension].append(new_name)


def transfer_file(file: Path, root_folder: Path, destination: str):
    """Функція, яка реалізує перенос файлів"""

    target_folder = Path(destination)
    target_folder.mkdir(exist_ok=True)
    file.replace(target_folder / file.name)


def delete_folder(folder: Path):
    """Функція видалення тек"""
    try:
        folder.rmdir()
    except OSError:
        print("Помилка видалення текі")


def main(folder: Path, destination: Path):
    """Основна логіка програми"""

    # сканування вибраної частини файлової системи, наповнення словника переносу і списку видалення
    scan(folder)
    # реалізація переносу файлів за словником переносу
    for ext, files in TRANSFER_DICT.items():
        for file in files:
            dest = destination / ext
            transfer_file(file, folder, dest)
    # видалення тек
    for f in FOLDERS:
        delete_folder(f)


if __name__ == "__main__":
    # вітання
    print(f'\n{"*"*10:^50}Welcome to sorter app!{"*"*10:^50}\n')

 
    # Створення парсера аргументів
    parser = argparse.ArgumentParser(description="Програма для сортування файлів")

    # Додавання аргументів
    parser.add_argument("source", help="Шлях до джерельного файлу")
    parser.add_argument("destination", help="Шлях до папки призначення")

    # Отримання аргументів
    args = parser.parse_args()

    # ввод, обробка і валідацію шляхів, введених користувачем
    while True:
        folder = Path(args.source)
        if folder.is_dir():
            try:
                destination = args.destination
                if not destination:
                    destination = Path.cwd() / "dist"
                else:
                    destination = Path(destination)
                destination.mkdir()
                break
            except:
                print("!!! Введіть вірний шлях до текі призначення !!!")
            else:
                print("!!! Введіть коректний шлях !!!")


    if not destination.is_absolute():
        print(f"Введено відносний шлях:\n {Path.cwd() / destination.name}")
    # реалізація основної логіки на веріфікованих шляхаха
    main(folder, destination)
    # завершення програми
    print(
        f"Сортування виконанно! Шукайте відсортовані по текам файли за наступним шляхом:\n{destination}"
    )
