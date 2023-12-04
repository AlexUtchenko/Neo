from pathlib import Path


FILENAME = Path(__file__).parent / "base.txt"


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            return "Give me name and phone please or only name for the PHONE command."
        except KeyError:
            return "Enter user name"

    return inner


def write_dict_file(path, data):
    with open(path, "w") as f:
        for name, number in data.items():
            s = f"{name}:{number}\n"
            f.write(s)


def read_dict_file(path):
    with open(path, "r") as f:
        data = f.readlines()
        res = {}
        for contact in data:
            name, phone = contact[:-1].split(":")
            res[name] = phone
        return res


def parser(string):
    elements = [x.strip() for x in string.split(" ")]
    elements[0] = elements[0].lower()
    return elements


@input_error
def add_contact(parsed, dict_base):
    _, name, phone = parsed
    if name not in dict_base:
        dict_base[name] = phone
        write_dict_file(FILENAME, dict_base)
        return "Contact added."
    else:
        return "This contact exists"


@input_error
def change_contact(parsed, dict_base):
    _, name, phone = parsed
    if name in dict_base:
        dict_base[name] = phone
        write_dict_file(FILENAME, dict_base)
        return "Contact updated."
    else:
        return "The contact doesn't exist."


@input_error
def show_phone(parsed, dict_base):
    _, name = parsed
    if name in dict_base:
        return dict_base[name]
    else:
        return "The contact doesn't exist."


def all(dict_base):
    if dict_base:
        res = ""
        count = 0
        for n, p in dict_base.items():
            count += 1
            res += "{:^3}|{:^12}|{:^12}\n".format(count, n, p)
        return res
    else:
        return "The phonebook is empty"


def handler(parsed, dict_base):
    command = parsed[0]
    if command == "hello":
        return "How can I help you?"
    if command in ["close", "exit"]:
        return "Good bye!"
    if command == "add":
        return add_contact(parsed, dict_base)
    if command == "change":
        return change_contact(parsed, dict_base)
    if command == "phone":
        return show_phone(parsed, dict_base)
    if command == "all":
        return all(dict_base)
    return "Invalid command."


def main():
    if FILENAME.exists():
        dict_base = read_dict_file(FILENAME)
    else:
        dict_base = {}
    print("Welcome to the assistant bot!")
    while True:
        command = input("Enter a command: ")
        parsed = parser(command)
        print(handler(parsed, dict_base))
        if parsed[0] in ["close", "exit"]:
            break


if __name__ == "__main__":
    main()
