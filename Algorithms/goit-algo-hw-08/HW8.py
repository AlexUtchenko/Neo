'''
Уявіть, що вам на технічному інтерв'ю дають наступну задачу, яку треба розв'язати за допомогою купи.
Є декілька мережевих кабелів різної довжини, їх потрібно об'єднати по два за раз в один кабель, використовуючи з'єднувачі, 
у порядку, який призведе до найменших витрат. Витрати на з'єднання двох кабелів дорівнюють їхній сумі довжин, а загальні витрати дорівнюють сумі з'єднання всіх кабелів.
Завдання полягає в тому, щоб знайти порядок об'єднання, який мінімізує загальні витрати.
'''

import heapq



def min_cost_cable_connection(cables):

    heapq.heapify(cables)
    min_cost = 0

    while len(cables) > 1:
        a = heapq.heappop(cables)
        b = heapq.heappop(cables)
        min_cost += a + b # min_cost буде сумою довжин усіх кабелів
        heapq.heappush(cables, a + b)

    return min_cost


cables = [1,2,3,4]
print(cables)

print(min_cost_cable_connection(cables))


