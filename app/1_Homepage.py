import streamlit as st
import pandas as pd
from utils import extract_df

nyc = extract_df.readshp("data/nyc-boundaries/geo_export_9ca5396d-336c-47af-9742-ab30cd995e41.shp")

st.set_page_config(
    page_title='NYC Taxi Fares Prediction Explorer',
    layout='wide'
)

st.title("NYC Taxi Fares Prediction Explorer")
st.markdown("Welcome to the Machine Learning project on predicting taxi fare amounts from New York City!")



uploaded_file = st.file_uploader('Upload your file here.')

# Save dataframe in streamlit session 
if uploaded_file:
    st.session_state['df'] = pd.read_csv(uploaded_file)
else:
    st.session_state['df'] =  extract_df.readcsv('data/taxi_data.csv')


st.markdown('The project was replicated by initiating the ETL (Extract Transform Load) process, followed by feature engineering, which involved clustering, incorporating temperature and trip distance. Next, we evaluated various models to determine the most effective one, ultimately selecting it to forecast taxi fare amounts. This process occurs in the backend. Subsequently, we will utilize Streamlit to visualize all components in the frontend.')
