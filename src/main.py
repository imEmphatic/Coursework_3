from utils import get_load_data_base, get_sorted_operations, print_operation

# количество выводимых операций
OPERATIONS_LEFT = 5


def main():
    """
    :return: Список из пяти операций
    """
    data = get_load_data_base('operations.json')

    list_ops = get_sorted_operations(data)[:OPERATIONS_LEFT]

    print(print_operation(list_ops))


if __name__ == '__main__':
    main()