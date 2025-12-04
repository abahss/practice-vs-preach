import pandas as pd
import os
from pathlib import Path
from practicepreach.constants import BUNDESTAG_WAHLPERIODE

def generate_manifesto_dataframe():
    """
    Generates a pandas DataFrame with columns: type, date, id, party, text
    - type: filled with 'manifesto' for all rows
    - date: exact start date of the wahlperiode that started in the year from filename (e.g., "2021-10-26")
    - id: party ID from filename before first underscore (e.g., "41113")
    - party: party name from parties_summary.csv based on ID
    - text: contains content from .txt files in german_manifestos folder
    """
    # Path to german_manifestos folder - handle both script and interactive execution
    try:
        # Try to use __file__ if available (when run as script)
        base_dir = Path(__file__).parent.parent
    except NameError:
        # Fall back to current working directory (when run interactively)
        base_dir = Path.cwd()

    manifestos_dir = base_dir / 'german_manifestos'

    # Load parties_summary.csv to map IDs to party names
    parties_summary_path = manifestos_dir / 'parties_summary.csv'
    parties_df = pd.read_csv(parties_summary_path)
    # Create a dictionary mapping party ID to party name
    party_id_to_name = dict(zip(parties_df['party'].astype(str), parties_df['name']))

    # Get all .txt files
    txt_files = sorted(manifestos_dir.glob('*.txt'))

    # Initialize lists for DataFrame
    data = {
        'type': [],
        'date': [],
        'id': [],
        'party': [],
        'text': []
    }

    # Read each .txt file and populate the DataFrame
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as f:
            text_content = f.read()

        # Extract ID from filename (e.g., "41113_202109_text.txt" -> "41113")
        filename = txt_file.stem  # Gets filename without extension
        filename_parts = filename.split('_')
        party_id = filename_parts[0]  # Get the part before first underscore

        # Extract year from filename (e.g., "41113_202109_text.txt" -> "2021")
        # Get the part after first underscore and take first 4 digits
        year_str = filename_parts[1][:4] if len(filename_parts) > 1 else ''

        # Find the wahlperiode that started in this year and get its start date
        wahlperiode_start_date = None
        if year_str:
            year_int = int(year_str)
            # Find wahlperiode where start date year matches
            for wahlperiode_num, (start_date, end_date) in BUNDESTAG_WAHLPERIODE.items():
                if start_date.year == year_int:
                    wahlperiode_start_date = start_date
                    break

        # Convert date to string format, or use empty string if not found
        date_str = wahlperiode_start_date.strftime('%d.%m.%Y') if wahlperiode_start_date else ''

        # Get party name from the mapping
        party_name = party_id_to_name.get(party_id, '')

        data['type'].append('manifesto')
        data['date'].append(date_str)
        data['id'].append(party_id)
        data['party'].append(party_name)
        data['text'].append(text_content)

    # Create DataFrame
    df = pd.DataFrame(data)

    # Write CSV to data folder (same folder as speeches-wahlperiode CSVs)
    data_dir = base_dir / 'data'
    csv_path = data_dir / 'manifestos.csv'
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"CSV written to: {csv_path}")

    return df



if __name__ == '__main__':
    df = generate_manifesto_dataframe()
    print(f"DataFrame created with {len(df)} rows")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nDataFrame shape: {df.shape}")
