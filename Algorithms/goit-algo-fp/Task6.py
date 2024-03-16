# реалізація жадібного алгоритму
def greedy_algorithm(items, budget):
    sorted_items = sorted(items.items(), key=lambda x: x[1]['calories'] / x[1]['cost'], reverse=True) # Сортування відношення калорійності до вартості
    selected_items = []
    total_cost = 0
    total_calories = 0

    for item, info in sorted_items: 
        if total_cost + info['cost'] <= budget:
            selected_items.append(item)
            total_cost += info['cost']
            total_calories += info['calories']

    return selected_items, total_cost, total_calories


# реалізація динамічного програмування
def dynamic_programming(items, budget):
    n = len(items)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]  # Таблиця динамічного програмування

    for i, (item, info) in enumerate(items.items(), 1):
        for j in range(budget + 1):
            if info['cost'] <= j:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - info['cost']] + info['calories'])
            else:
                dp[i][j] = dp[i - 1][j]

    selected_items = []
    j = budget
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            item, info = list(items.items())[i - 1]
            selected_items.append(item)
            j -= info['cost']

    total_cost = sum(items[item]['cost'] for item in selected_items)
    return selected_items, total_cost, dp[n][budget]



if __name__ == "__main__":

    # Вхідні дані
    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350}
    }

    budget = 100

    # Виклик жадібного алгоритму
    selected_items, total_cost, total_calories = greedy_algorithm(items, budget)

    print("Жадібний алгоритм:")
    print("Вибрані страви:", selected_items)
    print("Загальна вартість:", total_cost)
    print("Загальна кількість калорій:", total_calories)

    # Виклик алгоритму динамічного програмування
    selected_items_dp, total_cost_dp, total_calories_dp = dynamic_programming(items, budget)

    print("\nАлгоритм динамічного програмування:")
    print("Вибрані страви:", selected_items_dp)
    print("Загальна вартість:", total_cost_dp)
    print("Загальна кількість калорій:", total_calories_dp)
