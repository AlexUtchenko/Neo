def find_coins_greedy(amount, coins):

    """ Приклад жадібного алгоритму """

    result = {}
    for coin in sorted(coins, reverse=True):
        while amount >= coin:
            amount -= coin
            result[coin] = result.get(coin, 0) + 1
    return result


def find_min_coins(amount, coins):

    """ Приклад динамічного програмування знизу з використанням таблиці мемоізаціїї dp """

    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for j in range(coin, amount + 1):
            coins_used = dp[j - coin] + 1 # кількість монет, необхідних для видачі решти
            if coins_used < dp[j]:
                dp[j] = coins_used
    result = {}
    j = amount
    while j > 0:
        for coin in coins:
            if j >= coin and dp[j] == dp[j - coin] + 1:
                result[coin] = result.get(coin, 0) + 1
                j -= coin
                break
    return result


# Приклад використання
coins = [50, 20, 10, 5, 2, 1]
amount = 113

coins_greedy = find_coins_greedy(amount, coins)
print(f"Жадібний алгоритм: {coins_greedy}")

coins_min = find_min_coins(amount, coins)
print(f"Алгоритм динамічного програмування: {coins_min}")