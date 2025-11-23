from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера.
    Використовує жадібний підхід: сортує за пріоритетом, а потім упаковує
    у групи за принципом First Fit.

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    # Конвертація вхідних даних у dataclass об'єкти
    jobs = [PrintJob(**job) for job in print_jobs]
    printer_limits = PrinterConstraints(**constraints)

    # Сортування завдань за пріоритетом (від 1 - найвищий до 3 - найнижчий)
    jobs.sort(key=lambda x: x.priority)

    # Змінні для фінального результату
    final_print_order = []
    total_time_minutes = 0

    # Змінні для поточної групи (партії) друку
    current_batch = []
    current_batch_volume = 0.0

    for job in jobs:
        # Перевірка, чи можна додати завдання в поточну групу
        # 1. Перевірка кількості
        is_count_ok = len(current_batch) < printer_limits.max_items
        # 2. Перевірка об'єму
        is_volume_ok = (current_batch_volume + job.volume) <= printer_limits.max_volume

        if is_count_ok and is_volume_ok:
            # Додаємо в поточний батч
            current_batch.append(job)
            current_batch_volume += job.volume
        else:
            # Поточна партія заповнена. Друкуємо її.
            if current_batch:
                # Час друку партії = максимальний час серед моделей у партії
                batch_time = max(j.print_time for j in current_batch)
                total_time_minutes += batch_time
                # Додаємо ID до фінального списку
                final_print_order.extend([j.id for j in current_batch])

            # Починаємо нову партію з поточним завданням
            current_batch = [job]
            current_batch_volume = job.volume

    # Обробка останньої партії, якщо вона залишилась
    if current_batch:
        batch_time = max(j.print_time for j in current_batch)
        total_time_minutes += batch_time
        final_print_order.extend([j.id for j in current_batch])

    return {
        "print_order": final_print_order,
        "total_time": total_time_minutes
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}   # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")
    # Очікування: M1+M2 (250 об'єм, 2 шт) -> 120 хв. Потім M3 -> 150 хв. Разом 270.

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")
    # Очікування: Сортування -> M2(P1), M1(P2), M3(P3).
    # M2 (150) + M1 (100) = 250 об'єм <= 300, 2 шт. Час max(90, 120) = 120.
    # M3 (окремо) = 150 хв. Разом 270.

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")
    # Очікування: Сортування -> M1(P1), M2(P1), M3(P2).
    # M1 (250). M2 (200) не влазить (250+200 > 300).
    # Партія 1: [M1], час 180.
    # Партія 2: [M2]. Спробувати додати M3 (180). 200+180 > 300. Не влазить.
    # Партія 2: [M2], час 150.
    # Партія 3: [M3], час 120.
    # Разом: 180 + 150 + 120 = 450.

if __name__ == "__main__":
    test_printing_optimization()