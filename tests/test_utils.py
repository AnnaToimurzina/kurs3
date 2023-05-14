import pytest
from utils import read_file, operations_executed, format_dates, date_change, from_user, to_user, show_transactions
import os.path

data = os.path.join('./operation.json')

def test_read_file():
    result = read_file(data)
    assert isinstance(result, list)


def test_read_file_with_invalid_file_path():
    with pytest.raises(FileNotFoundError):
        assert read_file("../tests/operations.json") == "Файл не найден"


def test_load_data_with_invalid_json_data():
    data_invalid_json = os.path.join("./utils.py")
    with pytest.raises(ValueError):
        read_file(data_invalid_json)

def test_operations_executed():
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4, "state": "CANCELLED"},
    ]
    expected_result = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 3, "state": "EXECUTED"},
    ]

    # Вызываем функцию и проверяем результат
    result = operations_executed(data)
    assert result == expected_result

def test_format_dates():
    list = [{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364",
             "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
             "description": "Перевод организации", "from": "MasterCard 7158300734726758",
             "to": "Счет 35383033474447895560"},
            {"id": 441945886, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041",
             "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
             "description": "Перевод организации", "from": "Maestro 1596837868705199",
             "to": "Счет 64686473678894779589"}]
    list_sorted = [{"id": 441945886, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041",
                    "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод организации", "from": "Maestro 1596837868705199",
                    "to": "Счет 64686473678894779589"},
                   {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364",
                    "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод организации", "from": "MasterCard 7158300734726758",
                    "to": "Счет 35383033474447895560"}]
    assert format_dates(list) == list_sorted


def test_date_change():
    assert date_change("2019-04-04T23:20:05.206878") == "04.04.2019"


def test_from_user():
    assert from_user(None) == "XXXX XXXX XXXX XXXX"
    assert from_user("Mastercard 1234561278901234") == "Mastercard 1234 56** **** 1234"


def test_to_user():
    assert to_user("Mastercard 1234564278904321") == "Mastercard **4321"


def test_show_transactions():
    data = [{"id": 441945886, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041",
                    "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод организации", "from": "Maestro 1596837868705199",
                    "to": "Счет 64686473678894779589"}]
    expected_output = "------------------------------\n" \
                      "26.08.2019 Перевод организации\n" \
                      "Maestro 1596 83** **** 5199 --> Счет **9589\n" \
                      "31957.58 руб.\n"
    assert show_transactions(data) == expected_output
