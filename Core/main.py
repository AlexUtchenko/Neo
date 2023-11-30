from random import randrange


def get_numbers_ticket(min, max, quantity):
    l = []
    if min >= 1 and max <= 1000:
        while len(l) != int(quantity):
            x = randrange(min,max)
            if x not in l:
                l.append(x)
        l.sort()
        return l
    else:
        return []


print(get_numbers_ticket(1,20,5))

