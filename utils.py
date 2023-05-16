import json
from datetime import datetime
import os.path

def read_file(data):
    ''' ложим в переменную data все содержимое файла json'''
    if not os.path.isfile(data):
        raise FileNotFoundError("Файл не найден")
    try:
        with open(data, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("Файл содержит недопустимый формат данных")
    return data


def operations_executed(data):
    """
    Возвращает список отфильтрованных операции
    :param data: список всех операций
    :return: список операций "EXECUTED"
    """
    new_list = []
    for operation in data:
        if operation.get("state") == "EXECUTED":
            new_list.append(operation)
    return new_list

def format_dates(data):
    '''Сортируем по дате'''
    data = [trans for trans in data if trans]
    data = sorted(data, key=lambda x: x["date"], reverse=True)
    return data

def date_change(data):
    ''' Преобразует дату перевода в формат ДД.ММ.ГГГГ (пример: 14.10.2018).'''
    date_changed = datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%f')
    return date_changed.strftime('%d.%m.%Y')



def from_user(item):
    """Номер карты замаскирован и не отображается целиком в формате  XXXX XX** **** XXXX
    (видны первые 6 цифр и последние 4, разбито по блокам по 4 цифры, разделенных пробелом)"""
    if item is None:
        return "XXXX XXXX XXXX XXXX"
    elif "Счет" in item:
        split_string = item.split()
        account_name = split_string[0]
        account_number = split_string[1]
        return f"{account_name} **{account_number[-4:]}"

    elif "Visa Classic" in item:
        split_string = item.split()
        account_name = split_string[1]
        account_number = split_string[2]
        return f"Visa Classic {account_number[0:4]} {account_number[4:6]}{'** ' + ('*' * 4)} {account_number[-4:]}"

    else:
        split_string = item.split(' ')
        account_name = split_string[0]
        account_number = split_string[1]
        return f"{account_name} {account_number[0:4]} {account_number[4:6]}{'** ' + ('*' * 4)} {account_number[-4:]}"


def to_user(item):
    """Номер счета замаскирован и не отображается целиком в формате  **XXXX
       (видны только последние 4 цифры номера счета)"""
    if "Visa Classic" in item:
        split_string = item.split()
        account_name = split_string[1]
        account_number = split_string[2]
        return f"Visa Classic {account_number[0:4]} {account_number[4:6]}{'** ' + ('*' * 4)} {account_number[-4:]}"

    else:
        split_string = item.split(' ')
        account_name = split_string[0]
        account_number = split_string[1]
        return f"{account_name} {'*' * 2}{account_number[-4:]}"



def show_transactions(data):
    """вывод картинки транзакции """
    if data is None:
        return "ERROR 404"

    for transaction in data[:5]:
        print("-" * 30)
        print("{date} {description}\n".format(date=date_change(transaction['date']),
                                                  description=transaction['description']),
              "{from_} --> {to}\n".format(from_=from_user(transaction.get('from')),
                                              to=to_user(transaction['to'])),
              "{amount} {currency}\n".format(amount=transaction['operationAmount']['amount'],
                                                 currency=transaction['operationAmount']['currency']['name']))







