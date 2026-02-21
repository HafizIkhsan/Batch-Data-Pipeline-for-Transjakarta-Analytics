import pandas as pd
from config import database

def ingest_data(file_path, table_name):
    df = pd.read_csv(file_path)
    print(f"Ingesting data from {file_path} with {len(df)} records.")

    df.to_sql(
        table_name,
        database,
        if_exists='replace',
        index=False
    )

    print(f"Data ingested into table '{table_name}' successfully.")

if __name__ == "__main__":
    ingest_data('data/raw/dfTransjakarta.csv', 'bronze_layer')