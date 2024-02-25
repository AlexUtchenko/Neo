import timeit
import random
import pandas as pd


def insertion_sort(lst):
    lst = lst[:]
    for i in range(1, len(lst)):
        key = lst[i]
        j = i-1
        while j >=0 and key < lst[j] :
                lst[j+1] = lst[j]
                j -= 1
        lst[j+1] = key 
    return lst


def merge(left, right):
    merged = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1
    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1
    return merged


def merge_sort(arr):
    arr = arr[:]
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    return merge(merge_sort(left_half), merge_sort(right_half))


if __name__ == '__main__':
    # генеруємо випадкові дані та засекаємо час
    sizes = [10, 100, 1000, 10000]

    t_ms = []
    t_is = []
    t_sd = []
    t_s = []

    for size in sizes: 
        data = [random.randint(0, size) for _ in range(size)]
        t_ms.append(timeit.timeit(lambda: merge_sort(data), number=30))
        t_is.append(timeit.timeit(lambda: insertion_sort(data), number=30))
        t_sd.append(timeit.timeit(lambda: sorted(data), number=30))
        t_s.append(timeit.timeit(lambda: data.sort(), number=30))
    
    # створюємо таблицю результатів
    df = pd.DataFrame({
        'merge_sort': t_ms,
        'insertion_sort': t_is,
        'sorted': t_sd,
        'sort': t_s
    }, index=sizes)
    print(df)
