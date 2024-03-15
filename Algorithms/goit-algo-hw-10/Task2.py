import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as spi
import pandas as pd


# Визначення функції та межі інтегрування
def f(x):
    return -x ** 3 + 4 * x ** 2 + 5 * x + 20

# реалізація метода Монте-Карсло
def monte_carlo_integration(f, a, b, n):
    inside = 0
    y_max = max(map(f,np.linspace(a, b, n)))   
    for i in range(n):
        x = np.random.uniform(a, b)
        y = np.random.uniform(0, y_max)
        if y <= f(x):
            inside += 1
    return (b - a) * y_max * inside / n


if __name__ == '__main__':
    a = -1  # Нижня межа
    b = 4  # Верхня межа

    # Створення діапазону значень для x
    x = np.linspace(-5, 5, 400)
    y = f(x)

    # Обчислення інтегралу за допомогою scipy.integrate.quad та методу Монте-Карло
    result_scipy = spi.quad(f, a, b)
    print(f"Результат інтегрування Scipy: {result_scipy[0]}")
    result_mc = monte_carlo_integration(f, a, b, 10_000)
    print(f"Результат інтегрування Монте-Карло: {result_mc}")

    # випробування впливу кількості точок на результат інтегрування
    n = [10, 100, 1000, 10000, 100000]
    results = []
    for i in n:
        result = monte_carlo_integration(f, a, b, i)
        results.append(result)
    dif = np.array(results) - result_scipy[0]
    table = pd.DataFrame({'n': n, 'result': results, 'error': dif}, index=range(1, len(n)+1))
    print(table)

    # Створення графіка
    fig, ax = plt.subplots()

    # Малювання функції
    ax.plot(x, y, 'r', linewidth=2)

    # Заповнення області під кривою
    ix = np.linspace(a, b)
    iy = f(ix)
    ax.fill_between(ix, iy, color='gray', alpha=0.3)

    # Налаштування графіка
    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')

    # Додавання меж інтегрування та назви графіка
    ax.axvline(x=a, color='gray', linestyle='--')
    ax.axvline(x=b, color='gray', linestyle='--')
    ax.set_title('Графік інтегрування f(x) = - x ** 3 + 4 * x ** 2 + 5 * x + 20 від ' + str(a) + ' до ' + str(b))
    plt.grid()
    plt.show()


