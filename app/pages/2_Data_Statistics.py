import streamlit as st
import pandas as pd
from utils import extract_df, transform
import time

st.title("NYC Taxi Fares Prediction Explorer")

nyc = extract_df.readshp("data/nyc-boundaries/geo_export_9ca5396d-336c-47af-9742-ab30cd995e41.shp")

# Function to load data from session state [ChatGPT assisted]
def get_data():
    if 'df' in st.session_state:
        return st.session_state['df']
    else:
        return extract_df.readcsv('data/taxi_data.csv')

@st.cache
def stats_page(dataframe):
    if st.button("Transform Data"):
        progress_bar = st.progress(0, text='Data Transformation is in progress. Please wait.')
        transformed_data = transform.dataTransformation(
            df=dataframe, nyc=nyc
        ).transform()
        for perc_completed in range(100):
            time.sleep(0.05)
            progress_bar.progress(perc_completed + 1)
        st.success('Successfully transformed data')

        st.markdown("**You can preview transformed data statistics below.**")
        st.header('Descriptive Statistics')
        st.write(transformed_data.describe())
        st.header('Data Header')
        st.write(transformed_data.head())

        st.session_state['transformed_df'] = transformed_data

    else:
        st.header('Descriptive Statistics')
        st.write(dataframe.describe())
        st.header('Data Header')
        st.write(dataframe.head())


df = get_data()
stats_page(dataframe=df)
