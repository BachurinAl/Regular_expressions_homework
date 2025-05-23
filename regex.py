import re
import csv


# Читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

# Обрабатываем каждую запись, начиная со второй строки
for index in range(1, len(contacts_list)):
    contact = contacts_list[index]

    # Регулярные выражение для парсинга имени и телефона
    name_regex = r"'(\w*[А-Яа-я]+)'?,?\s?'?([А-Я][а-я]+)'?,?\s?'?(\w+)?'"
    name_matches = re.findall(name_regex, str(contact))
    phone_regex = r"(\+7|8)\s?\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d+)(\s\(?(доб.)\s?(\d+)\)?)?"

    # Обновляем поля контакта при успешном парсинге
    if name_matches:
        contact[0] = name_matches[0][0]
        contact[1] = name_matches[0][1]
        contact[2] = name_matches[0][2] if name_matches[0][2] else contact[2]

    # Обновляем телефонное поле при совпадении
    contact[5] = re.sub(phone_regex, r"+7(\2)\3-\4-\5 \7\8", contact[5]).strip()

    # Ограничиваем длину записи до 7 элементов
    if len(contact) > 7:
        del contact[7:]

# Объединяем дублирующиеся контакты по фамилии и имени
correct_contacts = [contacts_list[0]]
for current in contacts_list[1:]:
    last_name = current[0]
    first_name = current[1]
    for other in contacts_list[1:]:
        if last_name == other[0] and first_name == other [1]:
            for i in range(2, 7):
                if current[i] == '' and other[i] != '':
                    current[i] = other[i]
    if current not in correct_contacts:
        correct_contacts.append(current)

for contact in correct_contacts:
    while len(contact) > 0 and contact[-1] == '':
        contact.pop()

# Код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
    datawriter = csv.writer(f)
    datawriter.writerows(correct_contacts)
