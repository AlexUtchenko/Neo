# Використання легковажного образу Python 3.10
FROM python:3.11-slim

# Завдання робочої директорії в контейнері
WORKDIR /app

# Копіювання файлів залежностей і встановлення залежностей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіювання всього іншого в робочу директорію
COPY . .

EXPOSE 8000

# Запуск програми при старті контейнера
CMD [ "python", "main.py" ]