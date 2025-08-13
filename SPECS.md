# Whimsort Specifications

Whimsort is a command-line tool that allows users to sort CSV files based on their subjective comparison of rows.

## Features

- **Add and Sort:** Users can add a new row to a CSV file. The tool will then ask the user to compare the new row with existing rows to place it in the correct sorted position.
- **Reorder:** Users can re-sort an entire existing CSV file. The tool will iterate through the rows and ask for user comparison to determine the new order.
- **Header Support:** The tool can handle CSV files with or without a header row. The header row is not included in the sorting process.

## Flow

1. The user provides the path to a CSV file.
2. The user specifies whether the CSV file has a header.
3. The user chooses to either 'add' a new row or 'reorder' the entire file.
4. **If adding a row:**
   - The user provides the content for the new row.
   - The tool uses a binary insertion algorithm, prompting the user for comparisons to find the correct position for the new row.
   - The new row is inserted, and the file is saved.
5. **If reordering:**
   - The tool iterates through each row, treating the first row as the initial sorted list.
   - For each subsequent row, it uses the binary insertion algorithm to place it into the sorted portion of the list, prompting the user for comparisons.
   - After all rows are sorted, the file is saved.
