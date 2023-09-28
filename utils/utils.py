import os
import json
from datetime import datetime


def get_data(path=os.path.join("..", "data", "operations.json")):
    """
    Читает файл operations.json и возвращает загруженные данные.
    """
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def last_operations():
    """
    Получает последние 5 выполненных операций из данных.

    Возвращает cписок, содержащий последние 5 выполненных операций.
    """
    data = get_data()
    executed_operations = []
    for operation in data:
        if "state" in operation and operation["state"] == "EXECUTED":
            executed_operations.append(operation)
    # print(*executed_operations[-1:-6:-1], sep="\n")
    return executed_operations[-1:-6:-1]


def format_operation(operation, destination=''):
    """
    Форматирует заданную операцию и возвращает отформатированное строковое представление.

    Возвращает cтроковое представление операции
    """
    formatted_date = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')

    if operation['description'] == 'Перевод с карты на счет':
        #Здесь столкнулся с проблемой, что карты были разных банковских систем.
        #Пришлось распаковывать данные и запаковывать обратно
        source = operation.get('from', '').split(' ')
        *source_names, deposit = source
        source_names_str = ' '.join(source_names)
        masked_source = f"{source_names_str} {deposit[0:4]} {deposit[5:7]}** **** {deposit[-4:]}"
        masked_destination = f"**{operation.get('to', '')[-4:]}"
        destination = f"{masked_source} -> Счет {masked_destination}"

    elif operation['description'] == 'Перевод со счета на счет':
        masked_source = f"**{operation.get('from', '')[-4:]}"
        masked_destination = f"**{operation.get('to', '')[-4:]}"
        destination = f"Счет {masked_source} -> Счет {masked_destination}"

    elif operation['description'] == 'Открытие вклада':
        destination = f"Счет **{operation.get('to', '')[-4:]}"

    else:
        if operation['from'].startswith('Счет '):
            masked_source = f"**{operation.get('from', '')[-4:]}"
            masked_destination = f"**{operation.get('to', '')[-4:]}"
            destination = f"Счет {masked_source} -> Счет {masked_destination}"
        else:
            source = operation.get('from', '').split(' ')
            *source_names, deposit = source
            source_names_str = ' '.join(source_names)
            masked_source = f"{source_names_str} {deposit[0:4]} {deposit[5:7]}** **** {deposit[-4:]}"
            masked_destination = f"**{operation.get('to', '')[-4:]}"
            destination = f"{masked_source} -> Счет {masked_destination}"

    formatted_operation = (
        f"{formatted_date} {operation['description']}\n"
        f"{destination}\n"
        f"{operation['operationAmount']['amount']} {operation['operationAmount']['currency']['name']}"
    )

    return formatted_operation
