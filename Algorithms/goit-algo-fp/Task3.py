import heapq


def dijkstra(graph, start):

    # Ініціалізація відстаней та бінарної купи
    distances = {vertex: float("inf") for vertex in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_vertex = heapq.heappop(pq) # вилучення елемента з найменшою відстанню з купи

        # Перевірка, чи не завершено обхід
        if distances[current_vertex] < current_distance:
            continue

        # Оновлення відстаней до сусідніх вершин
        for neighbor, weight in graph[current_vertex].items():
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(pq, (new_distance, neighbor))

    return distances

if __name__ == "__main__":

    # Приклад графа у вигляді словника
    graph = {
        "A": {"B": 5, "C": 10},
        "B": {"A": 5, "D": 3},
        "C": {"A": 10, "D": 2},
        "D": {"B": 3, "C": 2, "E": 4},
        "E": {"D": 4},
    }

    # Виклик функції для вершини A
    print(dijkstra(graph, "A"))
