from utils import last_operations, format_operation

if __name__ == "__main__":
    for operation in last_operations():
        print(format_operation(operation), end="\n\n")