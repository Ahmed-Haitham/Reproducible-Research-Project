import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import unary_union
from shapely.geometry import Polygon

class dataTransformation:
    def __init__(self, df):
        self.df = df
    
    def deleteCols(self):
        unncessaryCols = ['id','key']
        self.df.drop(columns = unncessaryCols, inplace=True)

    def convertData(self):
        self.df['passenger_big_group'] = self.df['passenger_count'].apply(lambda x: 0 if x <= 4 else 1)
        self.df['passenger_big_group'] = self.df['passenger_big_group'].astype('category')
        self.df['fare_amount_log'] = np.log(self.df['fare_amount'])

    # Data Cleaning Pick Up missing Cords & Drop Off missing Cords

    # 01 generate random numbers in NYC boundaries
    def generateRandomPointsWithinPolygon(self, polygon, numPoints):
        points = []
        min_x, min_y, max_x, max_y = polygon.bounds
        while len(points) < numPoints:
            random_points = [Point(np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)) for _ in range(numPoints)]
            points.extend([point for point in random_points if polygon.contains(point)])
        return points[:numPoints]

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

        # Generate random coordinates for missing pickup points
        random_points_pickup = self.generateRandomPointsWithinPolygon(nycUnion, num_missingPickup)
        random_coordinates_pickup = np.array([(point.x, point.y) for point in random_points_pickup])
        # Generate random coordinates for missing dropoff points
        random_points_dropoff = self.generateRandomPointsWithinPolygon(nycUnion, num_missingDropoff)
        random_coordinates_dropoff = np.array([(point.x, point.y) for point in random_points_dropoff])

        # Impute the missing pickup and drop offs coordinates with random coordinates
        self.df.loc[missingPickup_coords, 'pickup_longitude'] = random_coordinates_pickup[:, 0]
        self.df.loc[missingPickup_coords, 'pickup_latitude'] = random_coordinates_pickup[:, 1]
        self.df.loc[missingDropoff_coords, 'dropoff_longitude'] = random_coordinates_dropoff[:, 0]
        self.df.loc[missingDropoff_coords, 'dropoff_latitude'] = random_coordinates_dropoff[:, 1]

    def transform(self):
        self.deleteCols()
        self.convertData()
        self.fillCoordinates()
        return self.df
