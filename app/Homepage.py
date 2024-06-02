import streamlit as st 
import pandas as pd 
import plotly.express as px
from utils import extract_df, transform, clustering, main, geoplots
import time 
import dask.dataframe as dd  # Import Dask for parallel processing

nyc = extract_df.readshp("data/nyc-boundaries/geo_export_9ca5396d-336c-47af-9742-ab30cd995e41.shp")

st.title('NYC Taxi Fares Prediction Explorer')
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
def transform_data(df):
    pass 

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
        st.subheader("Transformed Data")
        st.write(transformed_data.head())

    st.header('Data Header')
    st.write(dataframe.head())
    st.header('Descriptive Statistics')
    st.write(dataframe.describe())

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
    df_transform = load_data()
    df_transform = transform.dataTransformation(
            df=df_transform, nyc=nyc
        ).transform()

    # Slider for selecting date range
    # date_range = st.slider('Select a range of dates you would like to map:', 
    #                        min_value=pd.to_datetime(df_transform['pickup_datetime'].min()), 
    #                        max_value=pd.to_datetime(df_transform['pickup_datetime'].max()))

    sample_size = st.number_input('Insert sample size to visualize (from 0 to 1):', min_value=0, max_value=1, value=None)

    if sample_size:
        df_filtered = df_transform.sample(sample_size*df_transform.shape[0]) 

    else: 
        df_filtered = df_transform

    # # Filter DataFrame based on selected date range
    # df_filtered = df_transform[(df_transform['pickup_datetime'] >= date_range[0]) & (df_transform['pickup_datetime'] <= date_range[1])]
    # Select clustering method
    clustering_method = st.sidebar.selectbox('Select Clustering Method', ['None', 6])

    if clustering_method == 'None':

        # Map Scatter Plot with Plotly 
        fig = px.scatter_mapbox(df_filtered, 
                                lon='pickup_longitude', 
                                lat='pickup_latitude', 
                                #  color='passenger_count', 
                                opacity = 0.5,
                                zoom=8,  
                                hover_data=['passenger_count'], 
                                size = 'trip_distance', 
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

    else: 
        pass

else: 
    df = load_data()
    model_page(dataframe=df)
