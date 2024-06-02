import pandas as pd
import numpy as np
import geopandas as gpd
import shapefile

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
    def generateRandomPointsWithinPolygon(self, num_points,maparray):
            np.random.seed(4326)
            size = num_points
            min_longitude, max_longitude = maparray[:, 0].min(), maparray[:, 0].max()
            min_latitude, max_latitude = maparray[:, 1].min(), maparray[:, 1].max()
            random_longitudes = np.random.uniform(min_longitude, max_longitude, size)
            random_latitudes = np.random.uniform(min_latitude, max_latitude, size)
            random_coordinates = np.column_stack((random_longitudes, random_latitudes))
            return random_coordinates

    # 02 fill missing coordinates
    def fillCoordinates(self):
        
        # Read nyc polygon into array
        nyc_coordinates = []
        for shape_rec in self.nyc.shapeRecords():
            shape = shape_rec.shape
            if shape.shapeType == shapefile.POLYGON:
                for i in range(len(shape.parts)):
                    start = shape.parts[i]
                    end = shape.parts[i + 1] if i + 1 < len(shape.parts) else len(shape.points)
                    coords = shape.points[start:end]
                    for coord in coords:
                        nyc_coordinates.append([coord[0], coord[1]])
        nyc_coordinates = np.array(nyc_coordinates)

        ### pick up missings
        missingPickup_coords = (self.df['pickup_longitude'] == 0) | (self.df['pickup_longitude'] > -72) | (self.df['pickup_latitude'] == 0)
        num_missingPickup = sum(missingPickup_coords)

        ### drop of missings
        missingDropoff_coords = (self.df['dropoff_longitude'] == 0) | (self.df['dropoff_longitude'] < -75) | (self.df['dropoff_latitude'] == 0) | (self.df['dropoff_latitude'] > 42)
        num_missingDropoff = sum(missingDropoff_coords)

        # Generate random coordinates for missing pickup& dropoff points
        random_points_pickup = self.generateRandomPointsWithinPolygon(num_missingPickup, nyc_coordinates)
        random_points_dropoff = self.generateRandomPointsWithinPolygon(num_missingDropoff, nyc_coordinates)
        
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

     # Calculate trip distance
    def calculate_trip_distance(self):
        """ 
        Function to calculate Harvesine distance based on pickup and dropoff coordinates. 
        Author: Irena Zimovska
        """
        def haversine_distance(lat1, lon1, lat2, lon2):
            """
            Calculate the great-circle distance between two points 
            on the Earth's surface given their latitude and longitude
            in decimal degrees.
            """
            # Convert decimal degrees to radians
            lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

            # Haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
            c = 2 * np.arcsin(np.sqrt(a))
            
            # Radius of Earth in kilometers is 6371
            km = 6371 * c
            return km
        
        self.df['trip_distance'] = haversine_distance(self.df['pickup_latitude'], 
                                                       self.df['pickup_longitude'], 
                                                       self.df['dropoff_latitude'], 
                                                       self.df['dropoff_longitude'])


    def transform(self):
        self.deleteCols()
        self.convertData()
        self.fillCoordinates()
        self.extractDateTime()
        self.calculate_trip_distance()
        return self.df