import streamlit as st 
import pandas as pd 
import plotly.express as px
from utils import extract_df, transform, clustering, main, geoplots
import time 

nyc = extract_df.readshp("data/nyc-boundaries/geo_export_9ca5396d-336c-47af-9742-ab30cd995e41.shp")

st.set_page_config(
    page_title='NYC Taxi Fares Prediction Explorer'
)

st.title("NYC Taxi Fares Prediction Explorer")
st.markdown("Welcome to the Machine Learning project on predicting taxi fare amounts from New York City!")

st.sidebar.header('Data upload')
uploaded_file = st.sidebar.file_uploader('Upload your file here.')

st.sidebar.header("Navigation")
page_options = st.sidebar.radio('Pages', options = ['Data Statistics', 'Data Visualisation', 'Model Performance'])


def load_data():
    if uploaded_file: 
        df = pd.read_csv(uploaded_file)
    else: 
        df = extract_df.readcsv('data/taxi_data.csv')
    return df

@st.cache
def stats_page(dataframe): 
    # Button to trigger transformation
    if st.button("Transform Data"):
        # Progress bar
        progress_bar = st.progress(0, text = 'Data Transformation is in progress. Please wait.')
        transformed_data = transform.dataTransformation(
            df=df, nyc=nyc
        ).transform()
        for perc_completed in range(100):
            time.sleep(0.05)    
            progress_bar.progress(perc_completed+1)
        st.success('Successfully transformed data')
        
        # Print out summaries for edited data
        st.markdown("**You can preview transformed data statistics below.**")
        st.header('Descriptive Statistics')
        st.write(transformed_data.describe())
        st.header('Data Header')
        st.write(transformed_data.head())

    else: 
        st.header('Descriptive Statistics')
        st.write(dataframe.describe())
        st.header('Data Header')
        st.write(dataframe.head())

def visuals_page(dataframe, lon, lat): 
    pass

def model_page(dataframe): 
    pass

# Set the page updates 
if page_options == 'Data Statistics': 
    df = load_data()
    stats_page(dataframe=df)

elif page_options == 'Data Visualisation': 

    st.header('Map Visualisation')

    
    # 1. For visualisations the data is instantly transformed, to ensure that there are no ambiguous coordinates.
    
    df_transform = load_data()
    df_transform = transform.dataTransformation(
            df=df_transform, nyc=nyc
        ).transform()

    # 2. The section for user selections: chart option, clusters, sample customization, etc. 
    # Plot version
    plot_option = st.selectbox('Please select the map plot version:', options=['heatmap', 'scatter-mapbox', 'pydeck-chart'])

    # Buttons layout 
    col1, col2 = st.columns(2)
    with col1: 
        # Select sample size to draw
        sample_size = st.number_input('Insert sample size to visualize (from 0 to 1):', min_value=0, max_value=1, value=None)

    with col2: 
        # Select clustering method
        clustering_method = st.selectbox('Select Clustering Method', ['None', 6])

    # Filtering data frame based on selected options
    if sample_size:
        df_filtered = df_transform.sample(sample_size*df_transform.shape[0]) 
    else: 
        df_filtered = df_transform

    # Slider for selecting date range
    # date_range = st.slider('Select a range of dates you would like to map:', 
    #                        min_value=pd.to_datetime(df_transform['pickup_datetime'].min()), 
    #                        max_value=pd.to_datetime(df_transform['pickup_datetime'].max()))

    # Filter DataFrame based on selected date range
    # df_filtered = df_transform[(df_transform['pickup_datetime'] >= date_range[0]) & (df_transform['pickup_datetime'] <= date_range[1])]

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
                margin={"r":0,"t":0,"l":0,"b":0},
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
                                    opacity = 0.5,
                                    center=dict(lat=40.75, lon=-73.97),
                                    zoom=8,  
                                    hover_data=[variable], 
                                    # size = 'trip_distance', 
                                    #  color_continuous_scale='Tealgrn'
                                    )

            fig.update_layout(
                margin={"r":0,"t":0,"l":0,"b":0},
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

         

        else: 

            pass
            # df_clustered = clustering.pickUpCluster(df_transform).clusterCreated()

            # # Map Scatter Plot with Plotly 
            # fig = px.scatter_mapbox(df_filtered, 
            #                         lon='pickup_longitude', 
            #                         lat='pickup_latitude', 
            #                         #  color='passenger_count', 
            #                         opacity = 0.5,
            #                         zoom=5,  
            #                         hover_data=['passenger_count'], 
            #                         # size = 'trip_distance', 
            #                         color='pickup_cluster'
            #                         #  color_continuous_scale='Tealgrn'
            #                         )

            # fig.update_layout(
            #     margin={"r":0,"t":0,"l":0,"b":0},
            #     mapbox_style="open-street-map",
            #     legend=dict(
            #         orientation="h",
            #         yanchor="bottom",
            #         y=1.02,
            #         xanchor="right",
            #         x=1
            #     ))

            # st.plotly_chart(fig, use_container_width=True)

if st.button('Generate Plot'):
    map_plot(plot_option = plot_option, sample_size=sample_size, variable = variable, clustering_method=clustering_method)


else: 
    df = load_data()
    model_page(dataframe=df)
