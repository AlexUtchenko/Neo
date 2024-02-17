from collections import deque


def palindrome():
    deq = deque()
    data = input('Перевіремо чи рядок є поліндромом? \n>>> ')
    for c in data:
        if c != ' ':
            deq.append(c.lower())
    r = deq.copy()
    r.reverse()
    print(deq)
    print(r == deq)


palindrome()
