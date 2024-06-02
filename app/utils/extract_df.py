import pandas as pd
import numpy as np
import geopandas as gpd
import shapefile

def readcsv(filepath):
    return pd.read_csv(filepath)

def readshp(filepath):
    return shapefile.Reader(filepath)

