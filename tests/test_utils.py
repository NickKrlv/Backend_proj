from datetime import datetime
from utils.utils import get_data, format_operation, get_executed_operations, get_last_sorted_operations
import pytest
import os


@pytest.fixture(autouse=True)
def set_working_directory():
    project_directory = os.path.abspath(os.path.dirname(__file__))
    os.chdir(project_directory)


def test_get_data():
    assert len(get_data()) > 0


def test_get_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        get_data(path="test")


def test_len_get_last_sorted_operations(data_for_test):
    data = data_for_test
    data = sorted(data, key=lambda x: datetime.strptime(x["date"], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)
    assert len(get_last_sorted_operations(data)) == 5


def test_get_last_sorted_operations_empty():
    assert len(get_last_sorted_operations([])) == 0


def test_get_last_sorted_operations(data_for_test):
    data = data_for_test
    data = get_last_sorted_operations(data)
    assert data == [{'date': '2019-07-12T20:41:47.882230',
                     'description': 'Перевод организации',
                     'from': 'Счет 48894435694657014368',
                     'id': 522357576,
                     'operationAmount': {'amount': '51463.70',
                                         'currency': {'code': 'USD', 'name': 'USD'}},
                     'state': 'EXECUTED',
                     'to': 'Счет 38976430693692818358'},
                    {'date': '2019-04-04T23:20:05.206878',
                     'description': 'Перевод со счета на счет',
                     'from': 'Счет 19708645243227258542',
                     'id': 142264268,
                     'operationAmount': {'amount': '79114.93',
                                         'currency': {'code': 'USD', 'name': 'USD'}},
                     'state': 'EXECUTED',
                     'to': 'Счет 75651667383060284188'},
                    {'date': '2019-03-23T01:09:46.296404',
                     'description': 'Перевод со счета на счет',
                     'from': 'Счет 44812258784861134719',
                     'id': 873106923,
                     'operationAmount': {'amount': '43318.34',
                                         'currency': {'code': 'RUB', 'name': 'руб.'}},
                     'state': 'EXECUTED',
                     'to': 'Счет 74489636417521191160'},
                    {'date': '2018-12-20T16:43:26.929246',
                     'description': 'Перевод организации',
                     'from': 'Счет 10848359769870775355',
                     'id': 214024827,
                     'operationAmount': {'amount': '70946.18',
                                         'currency': {'code': 'USD', 'name': 'USD'}},
                     'state': 'EXECUTED',
                     'to': 'Счет 21969751544412966366'},
                    {'date': '2018-06-30T02:08:58.425572',
                     'description': 'Перевод организации',
                     'from': 'Счет 75106830613657916952',
                     'id': 939719570,
                     'operationAmount': {'amount': '9824.07',
                                         'currency': {'code': 'USD', 'name': 'USD'}},
                     'state': 'EXECUTED',
                     'to': 'Счет 11776614605963066702'}]


def test_get_executed_operations(data_for_test):
    data = data_for_test
    data = [operation for operation in data if "state" in operation and operation["state"] == "EXECUTED"]
    assert len(get_executed_operations(data)) == 6


def test_format_operation(data_for_test):
    data = data_for_test[0]
    assert format_operation(data) == "30.06.2018 Перевод организации\nСчет **6952 -> Счет **6702\n9824.07 USD"


def test_format_operation_internal_transfer():
    operation = {
        'date': '2022-01-01T12:00:00.000000',
        'description': 'Перевод со счета на счет',
        'from': 'Счет 1234 5678 9012 3456',
        'to': 'Счет 9876 5432 1098 7654',
        'operationAmount': {
            'amount': 200,
            'currency': {
                'name': 'USD'
            }
        }
    }
    expected_result = (
        '01.01.2022 Перевод со счета на счет\nСчет **3456 -> Счет **7654\n200 USD'
    )
    assert format_operation(operation) == expected_result


def test_get_executed_operations_empty():
    assert len(get_executed_operations([])) == 0


@pytest.fixture
def data_for_test():
    return [{
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    },
        {
            "id": 587085106,
            "state": "EXECUTED",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {
                "amount": "48223.05",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Открытие вклада",
            "to": "Счет 41421565395219882431"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 214024827,
            "state": "EXECUTED",
            "date": "2018-12-20T16:43:26.929246",
            "operationAmount": {
                "amount": "70946.18",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 10848359769870775355",
            "to": "Счет 21969751544412966366"
        },
        {
            "id": 522357576,
            "state": "EXECUTED",
            "date": "2019-07-12T20:41:47.882230",
            "operationAmount": {
                "amount": "51463.70",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 48894435694657014368",
            "to": "Счет 38976430693692818358"
        }]
