#!/usr/bin/env python3

import argparse
import csv
import sys

def get_user_comparison(item1, item2, header=None):
    """Prompts the user to compare two items."""
    while True:
        print("\nWhich item should be higher in the list?")
        if header:
            print(f"Header: {header}")
        print(f"1: {item1}")
        print(f"2: {item2}")
        choice = input("Enter 1 or 2: ").strip()
        if choice in ('1', '2'):
            return int(choice)
        print("Invalid input. Please enter 1 or 2.")

def binary_insert(sorted_list, item, compare_func):
    """Inserts an item into a sorted list using binary insertion."""
    low = 0
    high = len(sorted_list)

    while low < high:
        mid = (low + high) // 2
        comparison = compare_func(item, sorted_list[mid])
        if comparison == 1:
            high = mid
        else:
            low = mid + 1
    
    sorted_list.insert(low, item)

def read_csv(file_path):
    """Reads a CSV file and returns a list of rows."""
    try:
        with open(file_path, 'r', newline='') as csvfile:
            return list(csv.reader(csvfile))
    except FileNotFoundError:
        return []

def write_csv(file_path, data):
    """Writes data to a CSV file."""
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def add_row(file_path, new_row, has_header):
    """Adds a new row to the CSV file using binary insertion."""
    data = read_csv(file_path)
    header = None
    if has_header:
        header = data.pop(0)
    
    compare = lambda item1, item2: get_user_comparison(item1, item2, header)
    
    binary_insert(data, new_row, compare)
    if header:
        data.insert(0, header)
    write_csv(file_path, data)
    print(f"\nAdded new row: {new_row}")

def reorder_rows(file_path, has_header):
    """Reorders all rows in the CSV file."""
    data = read_csv(file_path)
    if not data:
        print("CSV file is empty. Nothing to reorder.")
        return

    header = None
    if has_header:
        header = data.pop(0)

    reordered_data = []
    for row in data:
        if not reordered_data:
            reordered_data.append(row)
        else:
            compare = lambda item1, item2: get_user_comparison(item1, item2, header)
            binary_insert(reordered_data, row, compare)

    if header:
        reordered_data.insert(0, header)
    write_csv(file_path, reordered_data)
    print("\nCSV file has been reordered.")

def main():
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(description="A CLI tool for sorting CSV files with user input.")
    parser.add_argument("file_path", help="Path to the CSV file.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'add' command
    add_parser = subparsers.add_parser("add", help="Add a new row to the CSV file.")
    add_parser.add_argument("row", nargs='+', help="The content of the new row.")
    add_parser.add_argument("--header", action="store_true", help="Treat the first row as a header.")

    # 'reorder' command
    reorder_parser = subparsers.add_parser("reorder", help="Reorder all rows in the CSV file.")
    reorder_parser.add_argument("--header", action="store_true", help="Treat the first row as a header.")

    args = parser.parse_args()

    if args.command == "add":
        add_row(args.file_path, args.row, args.header)
    elif args.command == "reorder":
        reorder_rows(args.file_path, args.header)

if __name__ == "__main__":
    main()
