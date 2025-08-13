import asyncio
import csv
from enum import Enum, auto

from ambler import amble

class Node(Enum):
    GET_CSV_PATH = auto()
    HAS_HEADER = auto()
    CHOOSE_ACTION = auto()
    GET_NEW_ROW = auto()
    SORT_ROW = auto()
    REORDER_ROWS = auto()
    SAVE_FILE = auto()
    END = auto()

def get_csv_path(state):
    """Gets the path to the CSV file from the user."""
    csv_path = input("Enter the path to the CSV file: ")
    state['csv_path'] = csv_path
    return state, Node.HAS_HEADER

def read_csv(state):
    """Reads the CSV file and populates the state."""
    with open(state['csv_path'], 'r') as f:
        reader = csv.reader(f)
        if state['has_header']:
            state['header'] = next(reader)
        state['data'] = list(reader)

def has_header(state):
    """Asks the user if the CSV file has a header."""
    response = input("Does the CSV file have a header? (y/n): ").lower()
    state['has_header'] = response == 'y'
    read_csv(state)
    return state, Node.CHOOSE_ACTION

def choose_action(state):
    """Asks the user whether they want to add a new row or reorder the file."""
    response = input("Do you want to 'add' a new row or 'reorder' the file?: ").lower()
    state['action'] = response
    if response == 'add':
        return state, Node.GET_NEW_ROW
    else:
        return state, Node.REORDER_ROWS

def get_new_row(state):
    """Gets the new row from the user."""
    new_row_str = input("Enter the new row (comma-separated values): ")
    state['new_row'] = new_row_str.split(',')
    return state, Node.SORT_ROW

def compare_rows(row1, row2):
    """Asks the user to compare two rows."""
    print(f"Which row is 'greater'?\n1: {row1}\n2: {row2}")
    while True:
        choice = input("Enter 1 or 2: ")
        if choice == '1':
            return 1  # row1 is greater
        elif choice == '2':
            return -1 # row2 is greater
        else:
            print("Invalid input. Please enter 1 or 2.")

def sort_row(state):
    """Sorts a new row into the existing data using binary insertion."""
    new_row = state['new_row']
    data = state['data']

    if not data:
        data.append(new_row)
        return state, Node.SAVE_FILE

    low = 0
    high = len(data) - 1
    insert_index = 0

    while low <= high:
        mid = (low + high) // 2
        comparison = compare_rows(new_row, data[mid])
        if comparison == 1:  # new_row is greater than data[mid], so new_row should be placed before data[mid]
            high = mid - 1
            insert_index = mid
        else:  # new_row is less than or equal to data[mid], so new_row should be placed after data[mid]
            low = mid + 1
            insert_index = low

    data.insert(insert_index, new_row)
    state['data'] = data
    return state, Node.SAVE_FILE

def reorder_rows(state):
    """Reorders the entire CSV file using binary insertion."""
    original_data = state['data']
    sorted_data = []

    for new_row in original_data:
        if not sorted_data:
            sorted_data.append(new_row)
            continue

        low = 0
        high = len(sorted_data) - 1
        insert_index = 0

        while low <= high:
            mid = (low + high) // 2
            comparison = compare_rows(new_row, sorted_data[mid])
            if comparison == 1:  # new_row is greater than sorted_data[mid], so new_row should be placed before sorted_data[mid]
                high = mid - 1
                insert_index = mid
            else:  # new_row is less than or equal to sorted_data[mid], so new_row should be placed after sorted_data[mid]
                low = mid + 1
                insert_index = low

        sorted_data.insert(insert_index, new_row)

    state['data'] = sorted_data
    return state, Node.SAVE_FILE

def save_file(state):
    """Saves the modified data back to the CSV file."""
    with open(state['csv_path'], 'w', newline='') as f:
        writer = csv.writer(f)
        if state['has_header'] and state['header']:
            writer.writerow(state['header'])
        writer.writerows(state['data'])
    print(f"File saved to {state['csv_path']}")
    return state, Node.END

async def direct(node, state):
    if node == Node.GET_CSV_PATH:
        return get_csv_path(state)
    elif node == Node.HAS_HEADER:
        return has_header(state)
    elif node == Node.CHOOSE_ACTION:
        return choose_action(state)
    elif node == Node.GET_NEW_ROW:
        return get_new_row(state)
    elif node == Node.SORT_ROW:
        return sort_row(state)
    elif node == Node.REORDER_ROWS:
        return reorder_rows(state)
    elif node == Node.SAVE_FILE:
        return save_file(state)
    elif node == Node.END:
        return state, None


async def main():
    """Main function to run the Whimsort application."""
    initial_state = {
        "csv_path": None,
        "has_header": None,
        "action": None,
        "new_row": None,
        "data": [],
        "header": None,
    }
    
    await amble(initial_state, Node.GET_CSV_PATH, direct)

if __name__ == "__main__":
    asyncio.run(main())
