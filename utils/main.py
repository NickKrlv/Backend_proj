from utils import get_data, get_last_sorted_operations, format_operation, get_executed_operations

if __name__ == "__main__":
    data = get_data()
    data = get_executed_operations(data)
    data = get_last_sorted_operations(data)
    for operation in data:
        print(format_operation(operation), end="\n\n")
