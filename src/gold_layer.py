import pandas as pd
from config import database

def gold_layer():
    df = pd.read_sql('SELECT * FROM silver_layer', database)

    print(f"Transforming data from silver_layer with {len(df)} records.")

    corridor_summary = (
        df.groupby('corridorID').agg(
            total_trips = ('transID', 'count'),
            avg_age = ('age', 'mean'),
            avg_trip_duration = ('trip_duration_minutes', 'mean'),
            total_revenue = ('payAmount', 'sum'),
            avg_revenue = ('payAmount', 'mean'),
            revenue_per_minute = ('payAmount', lambda x: (x.sum() / df.loc[x.index, 'trip_duration_minutes'].sum()) if df.loc[x.index, 'trip_duration_minutes'].sum() > 0 else 0)
        )
        .reset_index()
    )

    corridor_summary['traffic_share'] = (
        corridor_summary.total_trips / corridor_summary.total_trips.sum()
    )

    corridor_summary['revenue_share'] = (
        corridor_summary.total_revenue / corridor_summary.total_revenue.sum()
    )

    corridor_summary['duration_efficiency'] = (
        corridor_summary.avg_trip_duration / corridor_summary.avg_trip_duration.mean()
    )

    corridor_summary['volume_category'] = pd.qcut(
        corridor_summary.total_trips,
        q = 3,
        labels = ['Low', 'Medium', 'High'],
        duplicates = 'drop'
    )

    ranking = (
        corridor_summary
        .sort_values(by=['total_revenue', 'total_trips'], ascending=False)
        .reset_index(drop=True)
    )

    ranking.to_sql(
        'gold_layer',
        database,
        if_exists='replace',
        index=False
    )

if __name__ == "__main__":
    gold_layer()
