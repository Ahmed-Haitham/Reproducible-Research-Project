import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

class pickUpCluster:
    def __init__(self, df):
        self.df = df


    def optimumNoCluster(self):
        # code to have number of optimum cluster
        # instead of hardcoding it
        self.df

    def developCluster(self):
        kmeans = KMeans(n_clusters=6, random_state=555)
        kmeans.fit(self.df[['pickup_longitude', 'pickup_latitude']])
        self.df['pickup_cluster'] = kmeans.labels_
        self.df['pickup_cluster'] = self.df['pickup_cluster'].astype('category')

    def clusterCreated(self):
        self.optimumNoCluster()
        self.developCluster()
        return self.df