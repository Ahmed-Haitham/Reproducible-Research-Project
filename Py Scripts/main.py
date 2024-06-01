import pandas as pd
import geopandas as gpd
import numpy as np
import Extract
import Transform
import clustering

def main():

    # extract taxi_data.csv
    filepathcsv = "data/taxi_data.csv"
    df = Extract.readcsv(filepathcsv)

    # extract nyc.shp
    filepathshp ="data/nyc-boundaries/geo_export_9ca5396d-336c-47af-9742-ab30cd995e41.shp"
    nyc = Extract.readshp(filepathshp)

    # transform & data cleaning
    transformer = Transform.dataTransformation(df,nyc)
    transformedDf = transformer.transform()

    # feature engineering

    # clustering
    cluster = clustering.pickUpCluster(transformedDf)
    df = cluster.clusterCreated()
    print(df)
    print(df['pickup_cluster'].value_counts())



if __name__ == "__main__":
    main()
