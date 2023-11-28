import re


def find_all_phones(text):
    all = re.findall(r"\+380\(\d{2}\)\d{3}-\d{1,2}-\d{2,3}", text)
    result = []
    for var in all:
        if len(var) == 17:
            result.append(var)
        if len(var) == 18:
            result.append(var[:-1])
    return result

text = 'Irma +380(67)777-7-771 second +380(67)777-77-77 aloha a@test.com abc111@test.com.net +380(67)111-777-777+380(67)777-77-787'
print(find_all_phones(text))