import fnmatch
import pandas as pd

excel_path = "SCF_files/Secure Controls Framework (SCF) - 2024.4.xlsx"

def find_matching_sheet(file_path, pattern):
    # Load the Excel file
    excel_file = pd.ExcelFile(file_path)
    
    # Get all sheet names
    sheet_names = excel_file.sheet_names

    # Find the first sheet name that matches the pattern
    for sheet_name in sheet_names:
        if fnmatch.fnmatch(sheet_name, pattern):
            return sheet_name
    
    raise ValueError(f"No sheet matching the pattern '{pattern}' found in the Excel file.")

def read_scf_tab(path):
    matching_sheet = find_matching_sheet(path, pattern="SCF 20*")
    
    df = pd.read_excel(path, sheet_name=matching_sheet)
    
    return df