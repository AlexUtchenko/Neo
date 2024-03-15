import pulp


# Створення змінних
x = pulp.LpVariable('x', lowBound=0, cat = 'Integer')  # Кількість лимонаду
y = pulp.LpVariable('y', lowBound=0, cat = 'Integer')  # Кількість фруктового соку

# Створення проблеми
model = pulp.LpProblem('optimization_problem', pulp.LpMaximize)

# Цільова функція (максимізація загальної кількості продуктів)
model += x + y

# Обмеження на ресурси
model += 2*x + y <= 100  # Вода
model += x <= 50  # Цукор
model += x <= 30  # Лимонний сік
model += 2*y <= 40  # Фруктове пюре

# Розв'язання
model.solve()

# Виведення результатів
print(pulp.LpStatus[model.status])

print(f"\nРезультат:")
print("Лимонад:", x.varValue)
print("Фруктовий сік:", y.varValue)
print("Загальна кількість продуктів:", x.varValue + y.varValue)

