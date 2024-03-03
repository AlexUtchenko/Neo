'''
Завдання 3:

У граф додано ваги ребер, програмно реалізовано алгоритм Дейкстри для знаходження найкоротшого шляху в розробленому графі.
'''

import networkx as nx
import matplotlib.pyplot as plt
from Task1 import N


def dijkstra(graph, start):
    dist = {vertex: float('inf') for vertex in graph}  # мінімальна відстань до вершини за замовчення дорівняє бесконечній
    dist[start] = 0 # відстань до початкової вершини
    unvisited = set(graph.nodes())  # невідвідані вершини

    while unvisited: # поки є невідвідані вершини
        current_vertex = min(unvisited, key=dist.__getitem__) # вибираємо найменшу вершину за відстанню 
        unvisited.remove(current_vertex) # видаляємо цю вершину як вже відвідану

        for neighbor, weight in graph[current_vertex].items(): # для кожного сусіда вершини
            new_dist = dist[current_vertex] + weight['weight'] # знаходимо нову відстань

            if new_dist < dist[neighbor]: # якщо відстань менша ніж відстань до сусіда замінюємо її
                dist[neighbor] = new_dist

    return dist

# друкуємо всі результати
print(dijkstra(N, 'O1'))

# знаходимо відстанб до визначнного графа від початкового.abs
print(dijkstra(N, 'O1')['N2'])

# візуалізація графа для наочної перевірки
pos = nx.spring_layout(N, k=0.3, seed=40)
nx.draw(N, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=15, width=2)
labels = nx.get_edge_attributes(N, 'weight')
nx.draw_networkx_edge_labels(N, pos, edge_labels=labels)

plt.show()