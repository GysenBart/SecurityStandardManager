from datetime import datetime
import fnmatch
import pandas as pd
from app import db, app
from models import SecurityDomains, SecurityControls, SecurityStandards, Clausule, DomainStandardClausule

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

def proces_excel_data():
    
    df = read_scf_tab(excel_path)
    
    with app.app_context():
        for index, row in df.iterrows():
            # Create or get domain
            domain = SecurityDomains.query.filter_by(name=row['Domain']).first()
            if not domain:
                domain = SecurityDomains(name=row['Domain'])
                db.session.add(domain)
            
            # Process each standard column
            for column in df.columns:
                if column != 'Domain':
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
        
        db.session.commit()