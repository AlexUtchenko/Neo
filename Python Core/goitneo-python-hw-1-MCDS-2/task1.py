from datetime import datetime, timedelta
from collections import defaultdict

Sasha_BD = datetime(year=1988, month=12, day=7)
Katya_BD = datetime(year=1996, month=12, day=8)

users = [
    {"name": "Sasha", "birthday": Sasha_BD},
    {"name": "Katya", "birthday": Katya_BD},
]

def congratulate(users):
    """ The function shows week days if there are any birthday from the list next week"""
    final = defaultdict(list) # because the function returns a dict with default value list
    today = datetime.now()
    w = today.weekday()
    week_end = today + timedelta(days=6-w)
    next_week_end = week_end + timedelta(days=7)
    for person in users:
        BD = datetime(year=today.year, month=person["birthday"].month, day=person["birthday"].day)
        if week_end < BD < next_week_end:
                final[BD.strftime('%A')].append(person["name"])
    print(dict(final))


congratulate(users)