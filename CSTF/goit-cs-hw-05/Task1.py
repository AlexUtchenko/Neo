import asyncio
import aiopath
import aiofile
import argparse
import aioshutil
import logging


async def read_folder(source_path, output_path):
    # зчитуємо всі файли з папки source_path
    async for file_path in aiopath.Path(source_path).rglob("*"):
        if await file_path.is_file():  # вибираємо лише шляхи файлів
            await copy_file(file_path, output_path)


async def copy_file(file_path, output_path):
    # створюємо нові шляхи тек
    extension = file_path.suffix[1:]  # прибираємо крапку з розширення
    destination_folder = aiopath.Path(output_path) / extension

    # створюємо теки для кожного розширення
    try:
        await destination_folder.mkdir(parents=True, exist_ok=True)
    except OSError as err:
        logging.error("Помилка створення нової директорії", err)

    # створюємо нові шляхи для файлів
    destination_file_path = destination_folder / file_path.name

    # копіюємо файл
    try:
        await aioshutil.copyfile(file_path, destination_file_path)
        print(f"Copied {file_path.name} to {destination_folder}")
    except OSError as err:
        logging.error("Помилка копіювання файлу", err)


async def main(source_folder, output_folder):
    source_folder = await aiopath.Path(source_folder).resolve()
    output_folder = await aiopath.Path(output_folder).resolve()
    await read_folder(source_folder, output_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Async script to sort files by extension."
    )
    parser.add_argument(
        "source_folder", help="Source folder containing files to be sorted."
    )
    parser.add_argument(
        "output_folder", help="Output folder where sorted files will be stored."
    )
    args = parser.parse_args()

    asyncio.run(main(args.source_folder, args.output_folder))
