import re


def find_all_emails(text):
    all = re.findall(r"[a-zA-Z]{1}[a-zA-Z0-9_.]+@\w+.\w{2,}", text)
    result = []
    for mail in all:
        if mail.split("@")[1].count('.') == 1:
            result.append(mail)
    return result