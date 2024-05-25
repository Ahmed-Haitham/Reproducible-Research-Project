import pandas as pd
import numpy as np
import geopandas as gpd

def readcsv(filepath):
    return pd.read_csv(filepath)

def readshp(filepath):
    return gpd.read_file(filepath)

