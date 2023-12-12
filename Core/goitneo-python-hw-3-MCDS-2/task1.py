from collections import UserDict, defaultdict
from datetime import date, datetime, timedelta
import pickle
from pathlib import Path


DEFAULT_ADDRESS_BOOK_PATH = Path(__file__).parent / "base.txt"


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

    def __repr__(self):
        return str(self.value)


class Birthday:
    def __init__(self, value):
        self.value = value
        self.date_obj = None

    def validate(self):
        try:
            splitted = self.value.split(".")
            self.date_obj = date(
                year=int(splitted[2]), month=int(splitted[1]), day=int(splitted[0])
            )
            return True
        except:
            return False

    def __repr__(self):
        return (
            f"{self.date_obj.strftime('%d.%m.%Y')}"
            if self.validate()
            else "Incorrect date"
        )


class Phone(Field):
    def __init__(self, value):
        self.value = value

    def validate(self):
        return True if self.value.isdigit() and len(self.value) == 10 else False

    def __repr__(self):
        return f"{self.value}" if self.validate() else "Incorrect phone number"

    def __str__(self):
        return f"{self.value}" if self.validate() else "Incorrect phone number"


class Record:
    def __init__(self, name, phone=None):
        self.name = Name(name)
        if phone is None:
            self.phones = []
        else:
            number = Phone(phone)
            self.phones = []
            if number.validate():
                self.phones.append(number)
            else:
                return False

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
        if old in self.phones:
            self.phones[self.phones.index(old)] = new
        else:
            return "There is now such number"

    def find_phone(self, phone):
        number = Phone(phone)
        for el in self.phones:
            if el.value == number.value:
                return el.value
        return None

    def add_birthday(self, bd_date: str):
        bd = Birthday(bd_date)
        if bd.validate():
            self.birthday = bd
            return True
        else:
            return False

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, record):
        self.data.pop(record)

    def find(self, name):
        if name in self.data:
            return self.data[name]
        return "There is no the contact in the address book"

    def get_birthdays_per_week(self):
        users = []
        for rec_name, rec in self.data.items():
            if "birthday" in dir(rec):
                users.append({"name": rec_name, "birthday": rec.birthday.date_obj})
        final = defaultdict(
            list
        )  # because the function returns a dict with default value list
        today = datetime.now()
        w = today.weekday()
        week_end = today + timedelta(days=4 - w)
        next_week_end = week_end + timedelta(days=7)
        for person in users:
            birth_day = datetime(
                year=today.year,
                month=person["birthday"].month,
                day=person["birthday"].day,
            )
            if week_end < birth_day <= next_week_end:
                if birth_day.weekday() in [5, 6]:
                    final["Monday"].append(person["name"])
                else:
                    final[birth_day.strftime("%A")].append(person["name"])
        res = ""
        week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        normalized_day_order = [
            (week[i], final[week[i]]) for i in range(0, 5) if week[i] in final
        ]
        for item in normalized_day_order:
            day, l = item
            s = f"{day}: "
            for name in l:
                s += f"{name}, "
            s = s[:-2] + "\n"
            res += s
        return res[:-1]


def add_birthday(parsed, book):
    if len(parsed) == 3:
        name = parsed[1]
        bd = parsed[2]
        if name in book.data:
            if book.data[name].add_birthday(bd):
                return "The contactwas updated"
            else:
                return "Incorrect date format. Should be DD.MM.YYYY"
        else:
            return "There is no such contact in the address book"
    else:
        return "add-birthday [ім'я] [дата народження]"


def show_birthday(parsed, book):
    if len(parsed) == 2:
        name = parsed[1]
        if name in book.data:
            if "birthday" in dir(book.data[name]):
                return book.data[name].birthday
            else:
                return "The contact has empty birthday field"
        else:
            return "There is no such contact in the address book"
    else:
        return "show-birthday [ім'я]"


def birthdays(book):
    res = book.get_birthdays_per_week()
    if res:
        return res
    else:
        return "There is no birthdays for the next week."


def dump_address_book(path, address_book):
    with open(path, "wb") as f:
        pickle.dump(address_book, f)


def load_address_book(path):
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def all(book):
    if len(book) != 0:
        res = ""
        count = 0
        for contact in book.data.keys():
            count += 1
            res += "{:^3}|{:^12}|\n".format(count, contact)
        return res
    else:
        return "The address book is empty"


def add(parsed, book):
    if len(parsed) == 3:
        name = parsed[1]
        phone = parsed[2]
        if name not in book.data:
            try:
                book.add_record(Record(name, phone))
                return f"{name} was added to the address book."
            except:
                return "Phone validation error. 10 digits is a correct format"
        else:
            return "The contact exists."
    else:
        return "add [ім'я] [телефон]"


def change(parsed, book):
    if len(parsed) == 3:
        name = parsed[1]
        phone = Phone(parsed[2])
        if name in book.data:
            if phone.validate():
                book.find(name).phones[0] = phone
                return "The contact was updated"
            else:
                return "Incorrect number"
        else:
            return "The contact doesn't exist."
    else:
        return "change [ім'я] [новий телефон]"


def phone(parsed, book):
    if len(parsed) == 2:
        name = parsed[1]
        if name in book.data:
            return book.find(name).phones[0]
        else:
            return "The contact doesn't exist."
    else:
        return "phone [ім'я]"


def parser(string):
    elements = [x.strip() for x in string.split(" ")]
    elements[0] = elements[0].lower()
    return elements


def handler(parsed, book):
    command = parsed[0]
    if command == "hello":
        return "How can I help you?"
    if command in ["close", "exit"]:
        return "Good bye!"
    if command == "add":
        return add(parsed, book)
    if command == "add-birthday":
        return add_birthday(parsed, book)
    if command == "show-birthday":
        return show_birthday(parsed, book)
    if command == "birthdays":
        return birthdays(book)
    if command == "change":
        return change(parsed, book)
    if command == "phone":
        return phone(parsed, book)
    if command == "all":
        return all(book)
    return "Invalid command."


def main():
    book = load_address_book(DEFAULT_ADDRESS_BOOK_PATH)
    print("Welcome to the assistant bot!")
    while True:
        command = input(">>> Enter a command: ")
        parsed = parser(command)
        print(handler(parsed, book))
        if parsed[0] in ["close", "exit"]:
            dump_address_book(DEFAULT_ADDRESS_BOOK_PATH, book)
            break


if __name__ == "__main__":
    main()
