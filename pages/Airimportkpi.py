import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import openpyxl

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

st.set_page_config(layout='wide')
st.image('https://www.geneltransport.com.tr/wp-content/uploads/2021/03/logo-color.png')

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
        st.page_link("pages/Istanbul.py", label="Istanbul", icon="🏙️")
        st.page_link("pages/Mersin.py", label="Mersin",  icon="🏙️")
        st.page_link("pages/Izmir.py", label="Izmir",  icon="🏙️")
    with st.sidebar.expander("Air Trend Report ✈️"):
        st.page_link("pages/Air.py",label="Total", icon="📊") 
        st.page_link("pages/Airexportkpi.py",label="air-export-kpi", icon="📊") 
        st.page_link("pages/Airimportkpi.py",label="air-import-kpi", icon="📊") 

    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout("Logout", "sidebar")

    col1, col2 = st.columns(2)

    dataframe1 = pd.read_excel('reports/air_import_employee_kpis/count_per.xlsx')
    df = pd.DataFrame(dataframe1)

    # Create a pie chart using Plotly Express
    fig = px.pie(df, values='count', names='employee_name', title='Employee Count Distribution',width=500)


    with col1:
     st.plotly_chart(fig)

    dataframe2 = pd.read_excel('reports/air_import_employee_kpis/price_weigth_per.xlsx')
    df = pd.DataFrame(dataframe2)

    # Create a pie chart using Plotly Express
    fig = px.pie(df, values='price_weigth', names='employee_name', title='Employee Price-Weight Distribution',width=500)


    with col2:
     st.plotly_chart(fig)

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
