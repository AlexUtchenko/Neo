class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
    def __repr__(self):
        return f"{type(self).__name__}({self.value!r})"


class LinkedList:
    def __init__(self):
        self.head = None

    def __str__(self):
        if self.head is None:
            return "Список порожній"
        current = self.head
        result = ""
        while current:
            result += f"{current.value} -> "
            current = current.next
        return result[:-4]

    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current: Node = self.head
            while current.next:
                current = current.next
            current.next = new_node

    # Реверсування однозв'язного списку
    def reverse(self) -> None:
        """Реверсування однозв'язного списку."""
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    # Сортування вставками
    def sort_insertion(self):
        if self.head is None or self.head.next is None:
            return
        sorted_list = LinkedList()
        sorted_list.append(self.head.value)

        current: Node = self.head.next
        while current:
            value = current.value
            current = current.next

            node: Node = sorted_list.head
            while node:
                if value <= node.value:
                    break
                prev = node
                node = node.next

            if node is None:
                sorted_list.append(value)
            else:
                if node == sorted_list.head:
                    sorted_list.head = Node(value)
                    sorted_list.head.next = node
                else:
                    prev.next = Node(value)
                    prev.next.next = node

        self.head = sorted_list.head

    # Об'єднання двох відсортованих списків
    def merge(self, other_list):
        """Об'єднання двох відсортованих списків."""
        merged_list = LinkedList()
        current_1 = self.head
        current_2 = other_list.head

        while current_1 and current_2:
            if current_1.value <= current_2.value:
                merged_list.append(current_1.value)
                current_1 = current_1.next
            else:
                merged_list.append(current_2.value)
                current_2 = current_2.next

        while current_1:
            merged_list.append(current_1.value)
            current_1 = current_1.next

        while current_2:
            merged_list.append(current_2.value)
            current_2 = current_2.next

        self.head = merged_list.head


if __name__ == "__main__":
    list_1 = LinkedList()
    list_1.append(5)
    list_1.append(1)
    list_1.append(3)
    print(list_1)

    list_2 = LinkedList()
    list_2.append(6)
    list_2.append(4)
    list_2.append(2)
    list_2.append(8)
    print(list_2)

    list_1.reverse()
    list_2.reverse()
    print('\n Реверсуємо списки:')
    print(list_1)
    print(list_2)

    list_1.sort_insertion()
    list_2.sort_insertion()
    print('\n Сортуємо списки:')
    print(list_1)
    print(list_2)

    list_1.merge(list_2)
    print("\n Об'єднуємо списки:")
    print(list_1)