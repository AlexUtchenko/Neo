def dec(func):
    def inner(s):
        return f' Dear collegues!\n\n   {func(s)}\n\nBest regards,\nOleksandr.'
    return inner






@dec
def text(s:str):
    res = []
    for i in s.split('.'):
        v = i.strip()
        v = v.capitalize()
        res.append(v)
    print(res)
    return '. '.join(res)


s = 'dkfjkjf. dfjskddjf. djfnjdn'
print(text(s))
