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


def get_executed_operations(data):
    """Получает список операций и оставляет только выполненные."""
    data = [operation for operation in data if "state" in operation and operation["state"] == "EXECUTED"]
    return data


def get_last_sorted_operations(data):
    """Получает список операций и сортирует его по дате."""
    print(data)
    data = sorted(data, key=lambda x: datetime.strptime(x["date"], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)
    print(data)
    return data[0:5]
# get_last_sorted_operations(get_executed_operations(get_data()))

def format_operation(operation, destination=''):
    """
    Форматирует заданную операцию и возвращает отформатированное строковое представление.

    Возвращает cтроковое представление операции
    """
    formatted_date = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')

    if operation['description'] == 'Перевод с карты на счет':

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
