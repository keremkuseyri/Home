import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import openpyxl
import numpy as np
from streamlit_lightweight_charts import renderLightweightCharts
from datetime import datetime
import os
st.set_page_config(page_title='Genel Transport',page_icon="https://www.geneltransport.com.tr/wp-content/uploads/2021/03/favicon.png", layout='wide')
st.image('https://www.geneltransport.com.tr/wp-content/uploads/2021/03/logo-color.png')
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()
if st.session_state["authentication_status"]:

    

    with st.sidebar.expander("Sea Trend Report ⛴"):
        st.page_link("Home.py", label="Total", icon="📊" )
    with st.sidebar.expander("Air Trend Report ✈️"):
        st.page_link("pages/Air.py",label="Total", icon="📊")
    with st.sidebar.expander("Air Export KPI 🎯"):
        st.page_link("pages/Airexportkpi.py",label="Air Export KPI", icon="📊")
        st.page_link("pages/Airexporttarget.py", label="Target Export KPI", icon="🎯")
    with st.sidebar.expander("Air Import KPI 🎯"):
        st.page_link("pages/Airimportkpi.py",label="Air Import KPI", icon="📊")
        st.page_link("pages/Airimporttarget.py", label="Target Import KPI", icon="🎯")
    with st.sidebar.expander("Air Customer Report ✈️"):
        st.page_link("pages/Clientanalitics.py",label="Client Offer/Success Analysis", icon="📈")
        st.page_link("pages/Clientaircustomer.py",label="Client Air Customer Offer Analysis", icon="📈")
    with st.sidebar.expander("Air Import/Export Yearly 📊"):
         st.page_link("pages/testdb2.py", label="Air Import/Export Yearly 📊")

    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout("Logout", "sidebar")

    filenames = os.listdir('air_customer_outs')
    filenames_selected=st.selectbox("Select customer", options=filenames, index=0)
    dataframe8 = pd.read_csv(f'air_customer_outs/'+ filenames_selected )
    dataframe8['Date'] = pd.to_datetime(dataframe8['Date']).dt.strftime('%Y-%m-%d')


    # Now you can use x_values and y_values as you did before
    x_values = dataframe8['Date'].tolist()
    y_values = dataframe8['Count'].tolist()


    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        }
    }

    seriesLineChart = [{
        "type": 'Line',
        "data": [
            {"time": x, "value": y} for x, y in zip(x_values, y_values)
        ],
        "options": {}
    }]

    st.subheader(filenames_selected + "Date - Count")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line11')

elif st.session_state["authentication_status"] is False:


    st.error('Username/password is incorrect')
    st.session_state.clear()  # Clears the entire session state
    st.session_state["rerun_trigger"] = True

elif st.session_state["authentication_status"] is None:


    st.warning('Please enter your username and password')
    st.session_state.clear()  # Clears the entire session state
    st.session_state["rerun_trigger"] = True



