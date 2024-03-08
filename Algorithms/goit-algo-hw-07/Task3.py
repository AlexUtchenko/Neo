# Завдання 1

# Напишіть алгоритм (функцію), який знаходить суму всіх значень дереві пошуку або в AVL-дереві. 
# Візьміть будь-яку реалізацію дерева з конспекту чи з іншого джерела.

# створимо двійкове дерево
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

    def __str__(self, level=0, prefix="Root: "):
        ret = "\t" * level + prefix + str(self.val) + "\n"
        if self.left:
            ret += self.left.__str__(level + 1, "L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, "R--- ")
        return ret


# Створення дерева
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
root.right.right = Node(6)
root.right.right.right = Node(7)
root.right.right.left = Node(8)


values = [] # глобальна змінна для тимчасових значеннь


# створимо функція, яка знаходить суму всіх значень у дереві використовуючи прямий обхід
def traversal_sum(root):
    global values
    if root:
        values.append(root.val)
        traversal_sum(root.left)
        traversal_sum(root.right)
    result = sum(values)
    return result


print(f'Сума всіх значень у дереві: \n {root} дорівнює {traversal_sum(root)}')
