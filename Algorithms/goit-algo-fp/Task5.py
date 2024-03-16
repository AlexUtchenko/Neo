import uuid
import networkx as nx
import matplotlib.pyplot as plt


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

# Створення дерева
root = Node(0)
root.left = Node(4)
root.left.left = Node(5)
root.left.right = Node(10)
root.right = Node(1)
root.right.left = Node(3)

def depth_first_traversal(node, color_gradient):
    if node is None:
        return
    
    current_color = color_gradient.pop(0)
    node.color = current_color

    draw_tree(root)

    depth_first_traversal(node.left, color_gradient)
    depth_first_traversal(node.right, color_gradient)

def breadth_first_traversal(root, color_gradient):
    if root is None:
        return
    
    queue = [root]

    while queue:
        current_node = queue.pop(0)
        current_color = color_gradient.pop(0)
        current_node.color = current_color

        draw_tree(root)

        if current_node.left:
            queue.append(current_node.left)
        if current_node.right:
            queue.append(current_node.right)

# Оберемо градієнт кольорів від темного до світлого
color_gradient = ['#%02X%02X%02X' % (int(25 + i * (230/10)), int(25 + i * (230/10)), int(25 + i * (230/10))) for i in range(11)]

# Візуалізація обходів дерева
depth_first_traversal(root, color_gradient.copy())

# Скидуємо колір вузлів для наступного обходу
def reset_colors(node):
    if node is None:
        return
    node.color = "skyblue"
    reset_colors(node.left)
    reset_colors(node.right)

reset_colors(root)

# Візуалізуємо обхід в ширину
breadth_first_traversal(root, color_gradient.copy())

