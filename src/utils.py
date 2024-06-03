import json
import datetime


def get_load_data_base(path):
    """
    :param path: Выгружает данные из файла json.
    :return: Возвращает список операций из json.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return 'Файл не найден'


def get_executed(database):
    """
    :param database: спиок словарей json
    :return: Возвращает только выполненные транзакции
    """
    return [operation for operation in database if operation.get('state') == 'EXECUTED']


def get_sorted_operations(database):
    """
    :param database:  список словарей json
    :return: отсортированный список словарей по дате
    """
    return sorted(get_executed(database), key=lambda x: x['date'], reverse=True)


def get_normalize_date(old_date_dct):
    """
    :param old_date_dct: дата в исходном формате
    :return: дата в нужном формате
    """
    date = datetime.datetime.strptime(old_date_dct['date'], '%Y-%m-%dT%H:%M:%S.%f')
    return date.strftime('%d.%m.%Y')


def get_hide_number(number):
    """
    :param number: номер карты или счета
    :return: скрытый номер карты или счета
    """
    if len(number) == 16:
        return f'{number[:4]} {number[4:6]}** **** {number[-4:]}'
    elif len(number) == 20:
        return f'**{number[-4:]}'


def print_operation(sorted_list):
    """
    :param sorted_list: отсортированный список последних операций
    :return: строка из пяти последних операций
    """
    operation = ''
    for i in sorted_list:
        date = get_normalize_date(i)
        description = i["description"]
        currency = i["operationAmount"]["currency"]["name"]
        amount = i["operationAmount"]["amount"]
        to_name = i["to"].split()[0]
        to_number = i["to"].split()[-1]
        if i.get("from") is not None:
            from_name = ' '.join(i["from"].split()[:-1])
            from_number = i["from"].split()[-1]
            operation += f'''{date} {description}
{from_name} {get_hide_number(from_number)} -> {to_name} {get_hide_number(to_number)}
{amount} {currency}
'''
        else:
            from_name = 'Неизвестно'
            operation += f'''{date} {description}
{from_name} -> {to_name} {get_hide_number(to_number)}
{amount} {currency}

'''
    return operation