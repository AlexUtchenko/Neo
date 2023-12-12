from datetime import datetime, timedelta
from collections import defaultdict

Sasha_BD = datetime(year=1988, month=12, day=15)
Katya_BD = datetime(year=1996, month=12, day=5)

users = [
    {"name": "Sasha", "birthday": Sasha_BD},
    {"name": "Katya", "birthday": Katya_BD},
]


def congratulate(users):
    """The function shows week days if there are any birthday from the list next week"""
    final = defaultdict(
        list
    )  # because the function returns a dict with default value list
    today = datetime.now()
    w = today.weekday()
    week_end = today + timedelta(days=4 - w)
    next_week_end = week_end + timedelta(days=7)
    for person in users:
        BD = datetime(
            year=today.year, month=person["birthday"].month, day=person["birthday"].day
        )
        if week_end < BD <= next_week_end:
            if BD.weekday() in [5, 6]:
                final["Monday"].append(person["name"])
            else:
                final[BD.strftime("%A")].append(person["name"])
    res = ""
    for day, l in final.items():
        s = f"{day}: "
        for name in l:
            s += f"{name}, "
        s = s[:-2] + "\n"
        res += s
    print(res[:-1])


congratulate(users)
