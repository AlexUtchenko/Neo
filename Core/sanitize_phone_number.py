def sanitize_phone_number(phone):
    new_phone = phone.strip().removeprefix("+").replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    return new_phone

phone = ' +38(095)69-69-444'

print(sanitize_phone_number(phone))