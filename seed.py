import os
import django
import csv

# Django environment setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Constituency

def import_csv_data():
    csv_file_path = 'constituencies.csv' # Unga CSV file peru
    
    with open(csv_file_path, mode='r', encoding='cp1252') as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            # Table-la data-va save pandrom
            Constituency.objects.get_or_create(
                sl_no=row['Sl.No'],
                name=row['Constituency_Name'],
                winning_candidate_2021=row['2021_Winning_Candidate'],
                winning_party_2021=row['2021_Winning_Party'],
                district=row['District '].strip()
            )
            count += 1
            print(f"Added: {row['Constituency_Name']}")
        
        print(f"Successfully imported {count} constituencies!")

if __name__ == '__main__':
    print("Starting data import...")
    import_csv_data()