import os
import pandas as pd

def load_csv_files(directory):
    """Loads the list of CSV files in the directory."""
    return [f for f in os.listdir(directory) if f.endswith(".csv")]

def process_csv(file_path):
    """Processes the CSV file and returns a DataFrame."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise ValueError(f"Error processing {file_path}: {e}")
