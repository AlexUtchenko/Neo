dict_base = {}


def parser(string):
    elements = [x.strip().lower() for x in string.split(' ')]
    return elements


def add_contact(parsed):
    global dict_base
    if len(parsed) == 3:            
        if parsed[1] not in dict_base:
            dict_base[parsed[1]] = parsed[2]
            return 'Contact added.'
        else:
            return 'This contact exists'
    else:
        return f"add [ім'я] [номер телефону]"


def change_contact(parsed):
    global dict_base
    if len(parsed) == 3:            
        if parsed[1] in dict_base:
            dict_base[parsed[1]] = parsed[2]
            return 'Contact updated.'
        else:
            return 'There is no such contact'
    else:
        return f"change [ім'я] [номер телефону]"
    

def show_phone(parsed):
    global dict_base
    if len(parsed) == 2:            
        if parsed[1] in dict_base:
            return dict_base[parsed[1]]
        else:
            return 'There is no such contact'
    else:
        return f"phone [ім'я]"
    

def all():
    global dict_base
    if dict_base:
        res = ''
        count = 0
        for n, p in dict_base.items():
            count += 1
            res += '{:^3}|{:^12}|{:^12}\n'.format(count, n, p)
        return res
    else:
        return 'The phonebook is empty'


def handler(parsed):
    command = parsed[0]
    if command == 'hello':
        return "How can I help you?"
    if command == 'close' or command == 'exit':
        return "How can I help you?"
    if command == 'add':
        return add_contact()
    if command == 'change':
        return change_contact()
    if command == 'phone':
        return show_phone()
    if command == 'all':
        return show_all()