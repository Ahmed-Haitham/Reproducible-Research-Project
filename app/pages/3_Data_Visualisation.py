import streamlit as st
import pandas as pd
import plotly.express as px
from utils import extract_df, transform, clustering, geoplots
import pydeck as pdk 
import numpy as np 

nyc = extract_df.readshp("data/nyc-boundaries/geo_export_9ca5396d-336c-47af-9742-ab30cd995e41.shp")
st.title("NYC Taxi Fares Prediction Explorer")
st.header('Map Visualisation')
st.markdown('In this page you may explore spatial distribution of taxi rides. The plots are created with Plotly and pydeck packages.')


if 'transformed_df' not in st.session_state: 
    st.error('Please make sure that the data was transformed.')

else: 
    # Store the transformed data 
    df_transform = st.session_state['transformed_df']

    plot_option = st.selectbox('Please select the map plot version:', 
    options=['plotly-scatter-clustering', 'plotly-heatmap', 'pydeck-chart-density', 'pydeck-chart-directions'])
    
    geoplots.map_plot(plot_option=plot_option, df_transform=df_transform)

