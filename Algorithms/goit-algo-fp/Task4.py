import uuid
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор для кожного вузла

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)  # Використання id та збереження значення вузла
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

def draw_tree(tree_root):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}  # Використовуйте значення вузла для міток

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()

# функція створення графа-купи зі списка
def build_heap_tree(values):
    new_graph = Node(min(values))
    values.remove(min(values))

    # Функція для вставки елементу за алгоритмом BFS
    def insert_bfs(root, key):
        if root is None:
            return Node(key)
        
        # Використовуємо чергу для BFS
        queue = deque([root])
        while queue:
            current = queue.popleft()
            if current.left is None:
                current.left = Node(key)
                break
            elif current.right is None:
                current.right = Node(key)
                break
            else:
                # Якщо у поточного вузла є обидва діти, додаємо їх у чергу для обробки
                queue.append(current.left)
                queue.append(current.right)
        return root

    for _ in range(len(values)):
        heapq.heapify(values)
        candidate = heapq.heappop(values)
        new_graph = insert_bfs(new_graph, candidate)

    return new_graph


if __name__ == "__main__":

    # припустимо в нас є список, з якого хочемо побудувати купу
    l = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
    print(l)

    # cтворюємо heapified list з нашого списку
    heapq.heapify(l)
    print(l)

    # будуємо граф з heapified list
    heap_from_graph = build_heap_tree(l)

    # візуалізуємо цей граф
    draw_tree(heap_from_graph)