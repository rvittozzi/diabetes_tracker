import pandas as pd

def get_blood_sugar_data_from_csv(csv_file):
    try:
        df = pd.read_csv(csv_file)
        return df["Blood Sugar (mg/dL)"].tolist()
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
