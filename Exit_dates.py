import pandas as pd

def find_value_by_condition(excel_path, specified_variable):
    # Load the Excel file
    df = pd.read_excel(excel_path)
    
    # Initialize variable to store the previous value in the fourth column for comparison
    previous_value_in_fourth_column = None

    output= []

    # Loop through the DataFrame to find the matching condition
    for i in range(len(df)):
        # Check if the current row's third column matches the specified variable
        if df.iloc[i, 2] == specified_variable:
            # If this is not the first occurrence and the fifth column value has changed
            if previous_value_in_fourth_column is not None and df.iloc[i, 4] != previous_value_in_fourth_column:
                # Return the value in the first column of this row
                output.append((df.iloc[i, 2], df.iloc[i, 4], df.iloc[i, 1], df.iloc[i, 0]))
            # Update the previous value in the fifth column for the next comparison
            previous_value_in_fourth_column = df.iloc[i, 4]
    
    # If no matching condition is found, return None
    return output

def first_instances(excel_path,sheet = 0):
    # Load the Excel file, add `header=0` if your file has headers, or remove it if it doesn't
    df = pd.read_excel(excel_path,sheet, header=0)
    
    # Optional: Check for and drop rows where any of the required columns have NaN values
    df = df.dropna(subset=[df.columns[2], df.columns[1], df.columns[0]])

    # Dictionary to keep track of first instances
    first_occurrences = {}

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Get the value in the third column
        key = row[df.columns[2]]  # Use column names if known, e.g., 'Column_Name'

        # If the value has not been recorded yet, add it to the dictionary
        if key not in first_occurrences and not pd.isna(key):
            # Store the tuple (value in column 3, value in column 2, value in column 1)
            first_occurrences[key] = (row[df.columns[2]],row[df.columns[4]], row[df.columns[1]], row[df.columns[0]])

    # Return a list of all recorded first occurrences
    return list(first_occurrences.values())

def unique_values_in_third_row(excel_path):
    # Load the Excel file
    df = pd.read_excel(excel_path, header=None)
    
    # Select the third row (indexing starts at 0, so index 2 is the third row)
    third_row = df.iloc[2]
    
    # Get unique values from the third row
    unique_values = third_row.unique()
    
    # Return the unique values
    return unique_values

def get_exit_date(firm,excel_path,sheet):
    occurences = first_instances(excel_path,sheet)
    firm_index = [tup[0] for tup in occurences].index(firm)
    recent_year = occurences[0][-1]
    if occurences[firm_index][-1] == recent_year:
        return []
    return [occurences[firm_index]]

def all_exit_dates(firm, excel_path, sheet):
    return get_exit_date(firm, excel_path, sheet) + find_value_by_condition(excel_path, firm)

# Example usage:
excel_path = "/Users/lucasg17/Documents/GitHub/Health-Innovation/Master.xlsx"
sheet_name = 0
firm = 'SUTRO BIOPHARMA INC'
# result = find_value_by_condition(excel_path, specified_variable)
result = first_instances(excel_path,sheet_name)
print(result)
print(get_exit_date(firm,excel_path,sheet_name))
print(find_value_by_condition(excel_path,firm))
print(all_exit_dates(firm, excel_path, sheet_name))