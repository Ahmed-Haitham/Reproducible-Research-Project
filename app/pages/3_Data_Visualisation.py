import streamlit as st
import pandas as pd
import plotly.express as px
from utils import extract_df, transform

nyc = extract_df.readshp("data/nyc-boundaries/geo_export_9ca5396d-336c-47af-9742-ab30cd995e41.shp")
st.header('Map Visualisation')

if 'transformed_df' in st.session_state:

    df_transform = st.session_state['transformed_df']

    plot_option = st.selectbox('Please select the map plot version:', options=['heatmap', 'scatter-mapbox', 'pydeck-chart'])

    col1, col2 = st.columns(2)
    with col1:
        sample_size = st.number_input('Insert sample size to visualize (from 0 to 1):', min_value=0, max_value=1, value=None)

    with col2:
        clustering_method = st.selectbox('Select Clustering Method', ['None', 6])

    if sample_size:
        df_filtered = df_transform.sample(int(sample_size * df_transform.shape[0]))
    else:
        df_filtered = df_transform

    variable = st.selectbox('Select a feature set color in the map:', options=df_filtered.columns)

    def map_plot(plot_option, sample_size, variable, clustering_method):
        if plot_option == 'heatmap':
            fig = px.density_mapbox(df_filtered,
                                    lon='pickup_longitude',
                                    lat='pickup_latitude',
                                    z=variable,
                                    radius=10,
                                    center=dict(lat=40.75, lon=-73.97),
                                    zoom=8,
                                    mapbox_style="open-street-map",
                                    color_continuous_scale='matter')

            fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ))

            st.plotly_chart(fig, use_container_width=True)

        elif plot_option == 'scatter-mapbox':
            fig = px.scatter_mapbox(df_filtered,
                                    lon='pickup_longitude',
                                    lat='pickup_latitude',
                                    color=variable,
                                    opacity=0.5,
                                    center=dict(lat=40.75, lon=-73.97),
                                    zoom=8,
                                    hover_data=[variable])

            fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                mapbox_style="open-street-map",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ))

            st.plotly_chart(fig, use_container_width=True)

        elif plot_option == 'pydeck-chart':
            pass

    if st.button('Generate Plot'):
        map_plot(plot_option=plot_option, sample_size=sample_size, variable=variable, clustering_method=clustering_method)

else: 
    st.error('Please make sure that the data was tranformed.')