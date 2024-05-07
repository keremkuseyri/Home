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

    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout("Logout", "sidebar")

    dataframe1 = pd.read_csv("air_offer_outs/Acente_İHRACAT_activities_comparison.csv")

    # Convert 'Month' column to datetime values
    dataframe1['Month'] = pd.to_datetime(dataframe1['Month'])
    dataframe1['Month'] = dataframe1['Month'].dt.strftime('%Y-%m-%d')

    # Now you can use x_values and y_values as you did before
    x_values = dataframe1['Month'].tolist()
    y_values = dataframe1['Acceptance Rate'].tolist()

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

    st.subheader("Acenta İhracat Acceptance Rate-Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line')
    x_values = dataframe1['Month'].tolist()
    y_values = dataframe1['Accepted Activities'].tolist()
    y2_values = dataframe1['Total Activities'].tolist()

    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
            
        }
    }

    seriesLineChart = [
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y_values)
            ],
            "options": {"title": "Accepted Activities", "color": "orange"}
        },
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y2_values)
            ],
            "options": {"title": "Total Activities", "color": "blue"}
        }
    ]

    st.subheader("Acente İHRACAT Activities Comparison - Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line01')



    dataframe2 = pd.read_csv("air_offer_outs/Acente_İTHALAT_activities_comparison.csv")

    # Convert 'Month' column to datetime values
    dataframe2['Month'] = pd.to_datetime(dataframe2['Month'])
    dataframe2['Month'] = dataframe2['Month'].dt.strftime('%Y-%m-%d')

    # Now you can use x_values and y_values as you did before
    x_values = dataframe2['Month'].tolist()
    y_values = dataframe2['Acceptance Rate'].tolist()


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

    st.subheader("Acenta İthalat Acceptance Rate-Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line1')
    x_values = dataframe2['Month'].tolist()
    y_values = dataframe2['Accepted Activities'].tolist()
    y2_values = dataframe2['Total Activities'].tolist()

    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
            
        }
    }

    seriesLineChart = [
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y_values)
            ],
            "options": {"title": "Accepted Activities", "color": "orange"}
        },
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y2_values)
            ],
            "options": {"title": "Total Activities", "color": "blue"}
        }
    ]

    st.subheader("Acenta İTHALAT Activities Comparison - Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line02')

    dataframe3 = pd.read_csv("air_offer_outs/activities_comparison.csv")

    # Convert 'Month' column to datetime values and then to string format
    dataframe3['Month'] = pd.to_datetime(dataframe3['Month']).dt.strftime('%Y-%m-%d')

    # Now you can use x_values, y_values, and y2_values as you did before
    x_values = dataframe3['Month'].tolist()
    y_values = dataframe3['Accepted Activities'].tolist()
    y2_values = dataframe3['Total Activities'].tolist()

    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
            
        }
    }

    seriesLineChart = [
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y_values)
            ],
            "options": {"title": "Accepted Activities", "color": "orange"}
        },
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y2_values)
            ],
            "options": {"title": "Total Activities", "color": "blue"}
        }
    ]

    st.subheader("TOTAL Activities Comparison - Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line2')


    dataframe4 = pd.read_csv("air_offer_outs/Bizim_CROSS TRADE_activities_comparison.csv")
    dataframe4['Month'] = pd.to_datetime(dataframe4['Month']).dt.strftime('%Y-%m-%d')


    # Now you can use x_values and y_values as you did before
    x_values = dataframe4['Month'].tolist()
    y_values = dataframe4['Acceptance Rate'].tolist()


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

    st.subheader("Bizim CROSS TRADE Acceptance Rate-Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line4')



    # Convert 'Month' column to datetime values and then to string format


    # Now you can use x_values, y_values, and y2_values as you did before
    x_values = dataframe4['Month'].tolist()
    y_values = dataframe4['Accepted Activities'].tolist()
    y2_values = dataframe4['Total Activities'].tolist()

    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
            
        }
    }

    seriesLineChart = [
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y_values)
            ],
            "options": {"title": "Accepted Activities", "color": "orange"}
        },
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y2_values)
            ],
            "options": {"title": "Total Activities", "color": "blue"}
        }
    ]

    st.subheader("Bizim CROSS TRADE Activities Comparison - Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line3')

    dataframe5 = pd.read_csv("air_offer_outs/Bizim_İHRACAT_activities_comparison.csv")

    dataframe5['Month'] = pd.to_datetime(dataframe5['Month']).dt.strftime('%Y-%m-%d')


    # Now you can use x_values and y_values as you did before
    x_values = dataframe5['Month'].tolist()
    y_values = dataframe5['Acceptance Rate'].tolist()


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

    st.subheader("Bizim İHRACAT Acceptance Rate-Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line5')





    # Now you can use x_values, y_values, and y2_values as you did before
    x_values = dataframe5['Month'].tolist()
    y_values = dataframe5['Accepted Activities'].tolist()
    y2_values = dataframe5['Total Activities'].tolist()

    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
            
        }
    }

    seriesLineChart = [
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y_values)
            ],
            "options": {"title": "Accepted Activities", "color": "orange"}
        },
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y2_values)
            ],
            "options": {"title": "Total Activities", "color": "blue"}
        }
    ]

    st.subheader("Bizim İHRACAT Activities Comparison - Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line6')

    dataframe6 = pd.read_csv("air_offer_outs/Bizim_İTHALAT_activities_comparison.csv")

    dataframe6['Month'] = pd.to_datetime(dataframe6['Month']).dt.strftime('%Y-%m-%d')


    # Now you can use x_values and y_values as you did before
    x_values = dataframe6['Month'].tolist()
    y_values = dataframe6['Acceptance Rate'].tolist()


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

    st.subheader("Bizim İTHALAT Acceptance Rate-Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line7')

    # Now you can use x_values, y_values, and y2_values as you did before
    x_values = dataframe6['Month'].tolist()
    y_values = dataframe6['Accepted Activities'].tolist()
    y2_values = dataframe6['Total Activities'].tolist()

    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
            
        }
    }

    seriesLineChart = [
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y_values)
            ],
            "options": {"title": "Accepted Activities", "color": "orange"}
        },
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y2_values)
            ],
            "options": {"title": "Total Activities", "color": "blue"}
        }
    ]

    st.subheader("Bizim İTHALAT Activities Comparison - Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line8')

    dataframe7 = pd.read_csv("air_offer_outs/Forwarder_İHRACAT_activities_comparison.csv")

    dataframe7['Month'] = pd.to_datetime(dataframe7['Month']).dt.strftime('%Y-%m-%d')


    # Now you can use x_values and y_values as you did before
    x_values = dataframe7['Month'].tolist()
    y_values = dataframe7['Acceptance Rate'].tolist()


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

    st.subheader("Forwarder İHRACAT Acceptance Rate-Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line9')

    x_values = dataframe7['Month'].tolist()
    y_values = dataframe7['Accepted Activities'].tolist()
    y2_values = dataframe7['Total Activities'].tolist()

    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
            
        }
    }

    seriesLineChart = [
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y_values)
            ],
            "options": {"title": "Accepted Activities", "color": "orange"}
        },
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y2_values)
            ],
            "options": {"title": "Total Activities", "color": "blue"}
        }
    ]

    st.subheader("Forwarder İHRACAT Activities Comparison - Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line10')
    dataframe8 = pd.read_csv("air_offer_outs/Forwarder_İTHALAT_activities_comparison.csv")

    dataframe8['Month'] = pd.to_datetime(dataframe8['Month']).dt.strftime('%Y-%m-%d')


    # Now you can use x_values and y_values as you did before
    x_values = dataframe8['Month'].tolist()
    y_values = dataframe8['Acceptance Rate'].tolist()


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

    st.subheader("Forwarder İTHALAT Acceptance Rate-Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line11')

    x_values = dataframe8['Month'].tolist()
    y_values = dataframe8['Accepted Activities'].tolist()
    y2_values = dataframe8['Total Activities'].tolist()

    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
            
        }
    }

    seriesLineChart = [
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y_values)
            ],
            "options": {"title": "Accepted Activities", "color": "orange"}
        },
        {
            "type": 'Line',
            "data": [
                {"time": x, "value": y} for x, y in zip(x_values, y2_values)
            ],
            "options": {"title": "Total Activities", "color": "blue"}
        }
    ]

    st.subheader("Forwarder İTHALAT Activities Comparison - Month")

    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesLineChart
        }
    ], 'line12')



elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')