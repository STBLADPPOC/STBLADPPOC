# Function to convert worksheet to list of lists
def read_excel_to_list(pd, file_path, sheet_name=0):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        # Convert DataFrame rows to a list of lists
        lines = df.values.tolist()
        return lines
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
    
 # Function to slice values from lists of lists
def get_values(url_list):
    values = []
    for sublist in url_list:
        values.extend(sublist)
    return values[1::2]