'''
Завдання 1

Створіть граф за допомогою бібліотеки networkX для моделювання певної реальної мережі (наприклад, транспортної мережі міста, соціальної мережі, інтернет-топології).
Візуалізуйте створений граф, проведіть аналіз основних характеристик (наприклад, кількість вершин та ребер, ступінь вершин).
'''

import networkx as nx
import matplotlib.pyplot as plt

# зобразимо структуру хімічної сполуки никотинамид за допомогою графів
N = nx.Graph()

# додамо атоми, як вершини графа
N.add_nodes_from(["N1", "C1", "C2", "C3", "C4", "C5", "C6", "O1", "N2", "H1", "H2"])

# додамо зв'язки, як ребра графа
N.add_edges_from([("N1", "C1"), ("C1", "C2"), ("C2", "C3"), ("C3", "C4"), ("C4", "C5"), ("C5", "N1"), ("C2", "C6"), ("C6", "O1"), ("C6", "N2"), ("N2", "H1"), ("N2", "H2")])

# позначимо подвійні зв'язки
for edge in N.edges:
    N[edge[0]][edge[1]]['weight'] = 1

for edge in [("C1", "C2"), ("C3", "C4"), ("C5", "N1"), ("C6", "O1")]:
    N[edge[0]][edge[1]]['weight'] = 2


if __name__ == '__main__':
    num_nodes = N.number_of_nodes()
    num_edges = N.number_of_edges()
    is_connected = nx.is_connected(N)

    print(f"Кількість атомів: {num_nodes}, кількість зв'язків: {num_edges}, цілісність молекули: {is_connected}")

    # Візуалізація графа
    pos = nx.spring_layout(N, k=0.3, seed=40)
    nx.draw(N, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=15, width=2)
    labels = nx.get_edge_attributes(N, 'weight')
    nx.draw_networkx_edge_labels(N, pos, edge_labels=labels)

    plt.show()