'''
Завдання 2

Напишіть програму, яка використовує алгоритми DFS і BFS для знаходження шляхів у графі, який було розроблено у першому завданні.
Далі порівняйте результати виконання обох алгоритмів для цього графа, висвітлить різницю в отриманих шляхах. Поясніть, чому шляхи для алгоритмів саме такі.
'''


import networkx as nx
import matplotlib.pyplot as plt
from Task1 import N


def dfs(graph, start_vertex):
    visited = set()
    # Використовуємо стек для зберігання вершин
    stack = [start_vertex]  
    while stack:
        # Вилучаємо вершину зі стеку
        vertex = stack.pop()  
        if vertex not in visited:
            print(vertex, end=' ')
            # Відвідуємо вершину
            visited.add(vertex)
            # Додаємо сусідні вершини до стеку
            stack.extend(sorted(graph[vertex]))


def bfs(graph, start_vertex):
    visited = set()
    # Створюємо чергу
    queue = [start_vertex]  
    while queue:
        # Вилучаємо вершину зі черги
        vertex = queue.pop(0)  
        if vertex not in visited:
            print(vertex, end=' ')
            # Відвідуємо вершину
            visited.add(vertex)
            # Додаємо сусідні вершини до черги
            queue.extend(graph[vertex]) 


if __name__ == '__main__':
    # дослідимо молекулу по dfs і bfs алгоритму від атому кисню, як найбільлш електронегативного
    dfs(N, "O1")
    print()
    bfs(N, "O1")

    # Візуалізація графа
    pos = nx.spring_layout(N, k=0.3, seed=40)
    nx.draw(N, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=15, width=2)
    labels = nx.get_edge_attributes(N, 'weight')
    nx.draw_networkx_edge_labels(N, pos, edge_labels=labels)

    plt.show()