from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Phone(Field):
    def __init__(self, value):
        self.value = value

    def validate(self):
        return True if self.value.isdigit() and len(self.value) == 10 else False

    def __str__(self):
        return str(self.value)


class Record:
    def __init__(self, name, phone=None):
        self.name = name
        if phone is None:
            self.phones = []
        else:
            number = Phone(phone)
            self.phones = []
            if number.validate():
                self.phones.append(number)
            else:
                return 'Initialization error'

    def add_phone(self, phone):
        number = Phone(phone)
        if number.validate():
            self.phones.append(number)
        else:
            return 'Initialization error'


    def remove_phone(self, phone):
        pos = 0
        number = Phone(phone)
        for index, value in enumerate(self.phones):
            if value == number.value:
                pos = index
                break
        self.phones.pop(pos)


    def edit(self, old_number, new_number):
        old = Phone(old_number)
        new = Phone(new_number)
        pos = 0
        for index, value in enumerate(self.phones):
            if value == old:
                pos = index
                break
        self.phones[pos] = new

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}"


john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.remove_phone("5555555555")

print(john_record)