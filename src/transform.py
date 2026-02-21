import pandas as pd
from config import database
from datetime import datetime

def transform_bronze_to_silver():
    df = pd.read_sql('SELECT * FROM bronze_layer', database)

    print(f"Tranforming data from bronze_layer with {len(df)} records.")

    # Changing data types from object to datetime
    df['tapInTime'] = pd.to_datetime(df['tapInTime'])
    df['tapOutTime'] = pd.to_datetime(df['tapOutTime'])

    # Drop null values from tapOutTime and payAmount
    df = df[df['tapOutTime'].notna()]
    df = df[df['payAmount'].notna()]

    # Fill null values in categorical columns with 'Unknown'
    non_critical_column =['corridorID',
                      'corridorName',
                      'tapInStops',
                      'tapOutStops',
                      'tapOutStopsName']

    for i in non_critical_column:
        df[i] = df[i].fillna('UNKNOWN')
    
    # Feature Engineering
    # Calculating age of passengers
    current_year = datetime.now().year
    df['age'] = current_year - df['payCardBirthDate']

    # Calculating trip duration in minutes
    df['trip_duration_minutes'] = (
        (df["tapOutTime"] - df["tapInTime"]).dt.total_seconds() / 60
    )

    # Remove invalid duration
    df = df[(df['trip_duration_minutes'] > 0) &
            (df['trip_duration_minutes'] < 300)]

    # Save the transformed data to the silver layer
    df.to_sql(
        'silver_layer',
        database,
        if_exists='replace',
        index=False
    )

    print(f"Data transformed and saved to 'silver_layer' successfully.")

if __name__ == "__main__":
    transform_bronze_to_silver()