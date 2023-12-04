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
                return "Initialization error"

    def add_phone(self, phone):
        number = Phone(phone)
        if number.validate():
            self.phones.append(number)
        else:
            return "Initialization error"

    def remove_phone(self, phone):
        number = Phone(phone)
        obj = None
        for index, value in enumerate(self.phones):
            if value.value == number.value:
                obj = value
                break
        if obj:
            self.phones.remove(obj)
        else:
            return "There is now such number"

    def edit_phone(self, old_number, new_number):
        old = Phone(old_number)
        new = Phone(new_number)
        obj = None
        for index, value in enumerate(self.phones):
            if value.value == old.value:
                obj = value
                break
        if obj:
            self.phones[self.phones.index(obj)] = new
        else:
            return "There is now such number"

    def find_phone(self, phone):
        number = Phone(phone)
        for el in self.phones:
            if el.value == number.value:
                return el.value
        return None

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name] = record

    def delete(self, record):
        self.data.pop(record)

    def find(self, name):
        if name in self.data:
            return self.data[name]
        return "There is no the contact in the address book"

    # Створення нової адресної книги


book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
