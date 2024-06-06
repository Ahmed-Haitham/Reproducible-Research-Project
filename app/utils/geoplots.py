import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import plotly.express as px 
import streamlit as st
import utils.clustering as clustering 
import pydeck as pdk 


def map_plot(plot_option, df_transform):
    """
    Function for the visualisations page in streamlit. 

    Author: Irena Zimovska. 
    """
    if plot_option == 'plotly-heatmap':

        col1, col2 = st.columns(2)
        with col1:
            sample_size = st.slider('Sample percentage:', 0.0, 1.0, 0.1)

        if sample_size > 0:
            df_filtered = df_transform.sample(frac=sample_size)
        else:
            df_filtered = df_transform

        with col2:
            variable = st.selectbox('Select a feature to color the map:', options=df_filtered.columns)

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
                    x=1))

        st.plotly_chart(fig, use_container_width=True)

    elif plot_option == 'plotly-scatter-clustering':
        col1, col2 = st.columns(2)
        with col1:
            sample_size = st.slider('Sample percentage:', 0.0, 1.0, 0.1)

        if sample_size > 0:
            df_filtered = df_transform.sample(frac=sample_size)
        else:
            df_filtered = df_transform

        with col2:
            clustering_method = st.selectbox('Depict K-Means clustering:', ['None', 'Clustered'])

        if clustering_method == 'Clustered':
            df_filtered = clustering.pickUpCluster(df=df_filtered).clusterCreated()

            fig = px.scatter_mapbox(df_filtered,
                                        lon='pickup_longitude',
                                        lat='pickup_latitude',
                                        color='pickup_cluster',
                                        opacity=0.5,
                                        center=dict(lat=40.75, lon=-73.97),
                                        zoom=8)
        else: 
            fig = px.scatter_mapbox(df_filtered,
                                        lon='pickup_longitude',
                                        lat='pickup_latitude',
                                        opacity=0.5,
                                        center=dict(lat=40.75, lon=-73.97),
                                        zoom=8)

            fig.update_traces(marker=dict(color='#8900F8'))

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

    elif plot_option == 'pydeck-chart-density':

        col1, col2 = st.columns(2)
        with col1:
            sample_size = st.slider('Sample percentage:', 0.0, 1.0, 0.1)

        if sample_size > 0:
            df_filtered = df_transform.sample(frac=sample_size)
        
        else:
            df_filtered = df_transform

        with col2:
            variable = st.selectbox('Select a feature to color in the map:', options=df_filtered.columns)
            value_range = st.slider(f'Select range for {variable}', float(df_filtered[variable].min()), float(df_filtered[variable].max()), 
                                        (float(df_filtered[variable].min()), float(df_filtered[variable].max())))

        if value_range:
            df_filtered = df_filtered[df_filtered[variable].between(value_range[0], value_range[1])]

        # Define a custom color range
        COLOR_RANGE = [
                [240, 230, 24],   # F0E618
                [248, 194, 10],   # F8C20A
                [241, 160, 26],   # F1A01A
                [198, 100, 140],  # C6648C
                [208, 58, 214],   # D03AD6
                [200, 31, 255],   # C81FFF
                [137, 0, 248]     # 8900F8
            ]

        # Sample Pydeck map chart
        layer = pdk.Layer(
                'HexagonLayer',
                data=df_filtered,
                get_position='[pickup_longitude, pickup_latitude]',
                radius=100,
                elevation_scale=50,
                elevation_range=[0, 200],
                pickable=True,
                extruded=True,
                get_fill_color='[0, 255, 0, 160]',
                color_range=COLOR_RANGE
            )

        view_state = pdk.ViewState(
                latitude=40.75,
                longitude=-73.97,
                zoom=10,
                pitch=50,
            )

        r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{elevationValue}"})

        st.pydeck_chart(r)

    elif plot_option == 'pydeck-chart-directions':

        col1, col2 = st.columns(2)
        with col1:
            sample_size = st.slider('Sample percentage:', 0.0, 1.0, 0.1)
            st.markdown('Trip ending point pictured in purple.')

        if sample_size > 0:
            df_filtered = df_transform.sample(frac=sample_size)
        
        else:
            df_filtered = df_transform

        with col2:
            variable = st.selectbox('Select a feature to color in the map:', options=df_filtered.columns)
            value_range = st.slider(f'Select range for {variable}', float(df_filtered[variable].min()), float(df_filtered[variable].max()), 
                                        (float(df_filtered[variable].min()), float(df_filtered[variable].max())))

        if value_range:
            df_filtered = df_filtered[df_filtered[variable].between(value_range[0], value_range[1])]

        layer = pdk.Layer(
                "ArcLayer",
                data=df_filtered,
                get_width="S000 * 2",
                get_source_position=["pickup_longitude", "pickup_latitude"],
                get_target_position=["dropoff_longitude", "dropoff_latitude"],
                get_tilt=15,
                get_source_color=[241, 160, 26],
                get_target_color=[137, 0, 248],
                pickable=True,
                auto_highlight=True)

        view_state = pdk.ViewState(
                latitude=40.75,
                longitude=-73.97,
                zoom=10,
                pitch=50,
            )

        r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{elevationValue}"})

        st.pydeck_chart(r)

