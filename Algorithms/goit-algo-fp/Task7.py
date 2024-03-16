import random
import matplotlib.pyplot as plt
import pandas as pd


# імітація кидання 1 кубіка
def one_cube():
    return random.randint(1, 6)

# імітація кидання 2 кубіків і агрегація результатів (метод Монте-Карло)
def monte_carlo_simulation(num_trials):
    sums_count = {i: 0 for i in range(2, 13)}  # Ініціалізуємо лічильник для кожної можливої суми

    for _ in range(num_trials):
        step1 = one_cube()
        step2 = one_cube()
        total = step1 + step2
        sums_count[total] += 1

    probabilities = {key: value / num_trials for key, value in sums_count.items()}  # Обчислюємо ймовірності

    return probabilities


def plot_probabilities_multi(num_trials_list):
    plt.figure(figsize=(12, 8))  # Розмір малюнка

    for i, num_trials in enumerate(num_trials_list, 1):
        probabilities = monte_carlo_simulation(num_trials)
        plt.subplot(2, 2, i)
        plt.bar(probabilities.keys(), probabilities.values())
        plt.xlabel('Сума')
        plt.ylabel('Ймовірність')
        plt.title(f'Симуляція з {num_trials} кидків')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # виконуємо імітацію кидання 2 кубіків і агрегація результатів (метод Монте-Карло) на 10_000 кидків
    result = monte_carlo_simulation(100000)
    sums = []
    probability = []
    for key, value in result.items():
        sums.append(key)
        probability.append(value)
    
    # виводимо результати у форматі таблиці
    probability = [i * 100 for i in probability]
    theoretical_results = [2.78, 5.56, 8.33, 11.11, 13.89, 16.67, 13.89, 11.11, 8.33, 5.56, 2.78]
    difference = [round(abs(theoretical_results[i] - probability[i]),2) for i in range(len(probability))]
    df = pd.DataFrame({
        'sums': sums,
        'probability': probability,
        'difference': difference
    })
    print(df)

    # візуалізація результатів з різними кількістями кидків
    num_trials_list = [10, 100, 1000, 10000]
    plot_probabilities_multi(num_trials_list)
