from datetime import datetime
import fnmatch
import pandas as pd
import os
import glob
from config import excel_path
from app import db, app
from app.models import SecurityDomains, SecurityStandards, Clausule, DomainStandardClausule, SecurityControls
from openpyxl.utils import column_index_from_string
from openpyxl import load_workbook

def get_latest_file():
    """Get the latest Excel file matching the pattern."""
    files = glob.glob(excel_path)

    if not files:
        raise FileNotFoundError("No SCF file found.")

    # Sort by last modified time (newest last)
    files.sort(key=os.path.getmtime, reverse=True)

    latest_excel = files[0]
    print(f"Using latest SCF file: {latest_excel}")
    
    return latest_excel

def find_matching_sheet(file_path, pattern):
    """Find the first sheet in the Excel file that matches the given pattern."""
    excel_file = pd.ExcelFile(file_path)
    
    # Get all sheet names
    sheet_names = excel_file.sheet_names

    # Find the first sheet name that matches the pattern
    for sheet_name in sheet_names:
        if fnmatch.fnmatch(sheet_name, pattern):
            return sheet_name
    
    raise ValueError(f"No sheet matching the pattern '{pattern}' found in the Excel file.")

def read_scf_tab():
    """Read the SCF tab from the latest Excel file."""
    # Get the latest file path
    path = get_latest_file()
    # Find the first sheet that matches the pattern "SCF 20*"
    matching_sheet = find_matching_sheet(path, pattern="SCF 20*")
    
    df = pd.read_excel(path, sheet_name=matching_sheet)
    
    # Read header comments using openpyxl
    wb = load_workbook(path, data_only=True)
    ws = wb[matching_sheet]

    header_comments = {
        cell.value: cell.comment.text if cell.comment else None
        for cell in ws[1]  # Header row
        if cell.value is not None
    }
    
    return df, matching_sheet, header_comments


def proces_excel_data(start_col):
    
    start_col = "AB" # Remove after testing
    
    # Convert to zero-based index (excel AB = index 27)
    start_col_index = column_index_from_string(start_col) -1
    
    df, latest_version, header_comments = read_scf_tab()
    
    # Get the headers for the standards
    standards_headers = df.columns[start_col_index:]
    
    with app.app_context():
        # Load standards
        for col in standards_headers: 
            # Create or get standard
            standard = SecurityStandards.query.filter_by(name=col).first()
            if not standard:
                # Get comment if any
                comment = header_comments.get(col, None)
                standard = SecurityStandards(name=col, version=latest_version, description=comment)
                db.session.add(standard)
        
        # Load domains     
        for index, row in df.iterrows():
            # Create or get domain
            domain = SecurityDomains.query.filter_by(name=row['SCF Domain']).first()
            if not domain:
                domain = SecurityDomains(name=row['SCF Domain'], version=latest_version)
                db.session.add(domain)
        
            # Create or get control & description
            control = SecurityControls.query.filter_by(name=row['SCF Control']).first()
            if not control:
                control = SecurityControls(name=row['SCF Control'], version=latest_version, description=row["Secure Controls Framework (SCF)\nControl Description"])
                db.session.add(control)
                
        # Load controls
        
        """
        for index, row in df.iterrows():
            # Create or get domain
            domain = SecurityDomains.query.filter_by(name=row['SCF Domain']).first()
            if not domain:
                domain = SecurityDomains(name=row['SCF Domain'])
                db.session.add(domain)
            
            # Process each standard column
            for column in df.columns:
                if column != 'SCF Domain':
                    # Create or get standard
                    standard = SecurityStandards.query.filter_by(name=column).first()
                    if not standard:
                        standard = SecurityStandards(name=column)
                        db.session.add(standard)
                    
                    # Process clausules
                    if pd.notna(row[column]):
                        clausules = str(row[column]).split('\n')
                        for clausule_text in clausules:
                            # Assuming clausule format is "number - description"
                            parts = clausule_text.split(' - ', 1)
                            if len(parts) == 2:
                                number, description = parts
                                
                                # Create or get clausule
                                clausule = Clausule.query.filter_by(
                                    number=number.strip()
                                ).first()
                                
                                if not clausule:
                                    clausule = Clausule(
                                        number=number.strip(),
                                        description=description.strip()
                                    )
                                    db.session.add(clausule)
                                
                                # End previous relationship if exists
                                existing_rel = DomainStandardClausule.query.filter_by(
                                    domain_id=domain.id,
                                    standard_id=standard.id,
                                    clausule_id=clausule.id,
                                    end_date=None
                                ).first()
                                
                                if existing_rel:
                                    existing_rel.end_date = datetime.now()
                                
                                # Create new relationship
                                new_rel = DomainStandardClausule(
                                    domain=domain,
                                    standard=standard,
                                    clausule=clausule
                                )
                                db.session.add(new_rel)
        """
        db.session.commit()