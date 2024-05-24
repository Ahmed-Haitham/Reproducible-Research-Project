import pandas as pd
import numpy as np
import Extract
import Transform

def main():

    # extract csv
    filepath = "data/taxi_data.csv"
    df = Extract.readData(filepath)

    # transform
    transformer = Transform.dataTransformation(df)
    transformedDf = transformer.transform()


if __name__ == "__main__":
    main()
