import pandas as pd
import geopandas as gpd
import numpy as np
import Extract
import Transform
import clustering
import Feature_Engineering

def main():

    # extract taxi_data.csv
    tripspathcsv = "../data/taxi_data.csv"
    df = Extract.readcsv(tripspathcsv)

    # extract nyc.shp
    tripspathshp = "../data/nyc-boundaries/geo_export_9ca5396d-336c-47af-9742-ab30cd995e41.shp"
    nyc = Extract.readshp(tripspathshp)

    # transform & data cleaning
    transformer = Transform.dataTransformation(df,nyc)
    transformedDf = transformer.transform()

    # feature engineering
    transformedDf['trip_distance'] = transformedDf.apply(Feature_Engineering.calculate_distance, axis=1)

    # tempreature data
    temperature_df = pd.read_csv('../data/NYC_Weather_2016_2022.csv')
    merged_df = Feature_Engineering.add_temperature(transformedDf, temperature_df)

    # clustering
    cluster = clustering.pickUpCluster(merged_df)
    df = cluster.clusterCreated()
    print(df)
    print(df['pickup_cluster'].value_counts())



if __name__ == "__main__":
    main()
