import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import unary_union
from shapely.geometry import Polygon

class dataTransformation:
    def __init__(self, df,nyc):
        self.df = df
        self.nyc = nyc

    # Delete Cols and Convert Data
    
    def deleteCols(self):
        unncessaryCols = ['id','key']
        self.df.drop(columns = unncessaryCols, inplace=True)

    def convertData(self):
        self.df['passenger_big_group'] = self.df['passenger_count'].apply(lambda x: 0 if x <= 4 else 1)
        self.df['passenger_big_group'] = self.df['passenger_big_group'].astype('category')
        self.df['fare_amount_log'] = np.log(self.df['fare_amount'])

    # Data Cleaning Pick Up missing Cords & Drop Off missing Cords

    # 01 generate random numbers in NYC boundaries
    def generateRandomPointsWithinPolygon(self, polygon, num_points):
        min_x, min_y, max_x, max_y = polygon.bounds
        random_points = np.random.uniform((min_x, min_y), (max_x, max_y), size=(num_points, 2))
        return random_points

    # 02 fill missing coordinates
    def fillCoordinates(self):
        # Generate random coordinates for imputation within the NYC boundaries
        nycUnion = unary_union(self.nyc.geometry)

        ### pick up missings
        missingPickup_coords = (self.df['pickup_longitude'] == 0) | (self.df['pickup_longitude'] > -72) | (self.df['pickup_latitude'] == 0)
        num_missingPickup = sum(missingPickup_coords)

        ### drop of missings
        missingDropoff_coords = (self.df['dropoff_longitude'] == 0) | (self.df['dropoff_longitude'] < -75) | (self.df['dropoff_latitude'] == 0) | (self.df['dropoff_latitude'] > 42)
        num_missingDropoff = sum(missingDropoff_coords)

        # Generate random coordinates for missing pickup& dropoff points
        random_points_pickup = self.generateRandomPointsWithinPolygon(nycUnion, num_missingPickup)
        random_points_dropoff = self.generateRandomPointsWithinPolygon(nycUnion, num_missingDropoff)
        
        # Impute the missing pickup and drop offs coordinates with random coordinates
        self.df.loc[missingPickup_coords, 'pickup_longitude'] = random_points_pickup[:, 0]
        self.df.loc[missingPickup_coords, 'pickup_latitude'] = random_points_pickup[:, 1]
        self.df.loc[missingDropoff_coords, 'dropoff_longitude'] = random_points_dropoff[:, 0]
        self.df.loc[missingDropoff_coords, 'dropoff_latitude'] = random_points_dropoff[:, 1]
    # Extract datetime features

    def extractDateTime(self):
        self.df['pickup_datetime'] = pd.to_datetime(self.df['pickup_datetime'])
        self.df['year'] = self.df['pickup_datetime'].dt.year
        self.df['month'] = self.df['pickup_datetime'].dt.month
        self.df['day'] = self.df['pickup_datetime'].dt.day
        self.df['hour'] = self.df['pickup_datetime'].dt.hour


    def transform(self):
        self.deleteCols()
        self.convertData()
        self.fillCoordinates()
        self.extractDateTime()
        return self.df
