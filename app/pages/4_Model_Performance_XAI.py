import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from utils import extract_df, transform
import shap 
import matplotlib.pyplot as plt 

st.title("NYC Taxi Fares Prediction Explorer")
st.header('ML Models Performance')

tab1, tab2 = st.tabs(["Cross Validation Metrics", "eXplainable ML"])

with tab1: 
    st.markdown('Original RMSE for XgBoost model is 0.143.')
    option = st.selectbox('Select the model of interest:', options=['RF_log', 'RF', 'XGB_log', 'XGB'])

    import pickle
    with open(f"../model/saved_models/cv_summaries/cv_summary_{option}.pkl", "rb") as input_file:
        cv_summary = pickle.load(input_file)

    st.dataframe(cv_summary)

with tab2:     
    with open(f"data/models/shap_values_XGB.pkl", "rb") as input_file:
        shap_values_pkl = pickle.load(input_file)

    col1, col2 = st.columns(2)
    with col1:
        chart_option_1 = st.selectbox('Select the model of interest:', options=['waterfall', 'bar', 'beeswarm', 'single_feature'])

    shap.initjs()

    if chart_option_1 == 'waterfall':
        st.subheader('Shapley Waterfall Plot')
        fig, ax = plt.subplots()
        # shap.initjs()
        shap.waterfall_plot(shap_values_pkl[0])
        st.pyplot(fig)


    elif chart_option_1 == 'bar': 
        st.subheader('Feature Importance')
        fig, ax = plt.subplots()
        #summary_plot_bar
        shap.plots.bar(shap_values_pkl[0])
        st.pyplot(fig)

    elif chart_option_1 == 'beeswarm': 
        # summarize the effects of all the features
        st.subheader('Beeswarm plot')
        fig, ax = plt.subplots()
        shap.plots.beeswarm(shap_values_pkl)
        st.pyplot(fig)
    
    elif chart_option_1 == 'single_feature': 
        st.subheader('Feature Importance')
        variable = st.selectbox('Select the feature of interest:', options=shap_values_pkl.feature_names)
        fig, ax = plt.subplots()
        shap.plots.scatter(shap_values_pkl[:, variable], color=shap_values_pkl)
        st.pyplot(fig)

    



    
