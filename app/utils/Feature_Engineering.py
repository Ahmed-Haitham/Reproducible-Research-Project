import pandas as pd
import numpy as np
from geopy.distance import distance

# Function to calculate distance
def calculate_distance(trip):
    pickup_coords = (trip['pickup_latitude'], trip['pickup_longitude'])
    dropoff_coords = (trip['dropoff_latitude'], trip['dropoff_longitude'])
    return distance(pickup_coords, dropoff_coords).km

# Function to add temperature
def add_temperature(trips_df, temperature_df):

    # Convert 'time' to datetime and extract date
    temperature_df['time'] = pd.to_datetime(temperature_df['time'])
    temperature_df['date'] = temperature_df['time'].dt.date

    # Calculate the daily average temperature
    daily_avg_temp = temperature_df.groupby('date')['temperature_2m (°C)'].mean().reset_index()
    daily_avg_temp.rename(columns={'temperature_2m (°C)': 'avg_temperature_2m (°C)'}, inplace=True)

    # Ensure the trips DataFrame has a 'pickup_datetime' column in datetime format
    trips_df['pickup_datetime'] = pd.to_datetime(trips_df['pickup_datetime'])

    # Extract the date part from 'pickup_datetime'
    trips_df['date'] = trips_df['pickup_datetime'].dt.date

    # Merge the trips DataFrame with the daily average temperature data
    merged_df = pd.merge(trips_df, daily_avg_temp, on='date', how='left')

    return merged_df