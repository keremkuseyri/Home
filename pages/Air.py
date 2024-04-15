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


    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout("Logout", "sidebar")



    dataframe1 = pd.read_excel('reports/air_raw_data/date_price_weigth.xlsx')
    dataframe2 = pd.read_excel('reports/air_forecasting/date_price_weigth.xlsx')

    # Display dataframes
    st.title("Price Weight")


    # Merge dataframes
    merged_df = pd.concat([dataframe1, dataframe2], ignore_index=True)

    # Convert 'date' column to datetime format
    merged_df['date'] = pd.to_datetime(merged_df['date'])

    # Add IsFuture column
    merged_df['IsFuture'] = merged_df['date'] > pd.Timestamp.now()

    # Create plot
    fig = px.line(merged_df, x='date', y='data', title='Date Price Weight', width=1000, color='IsFuture',
                color_discrete_map={True: 'green', False: 'blue'})
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Price Weight')

    # Show plot
    st.plotly_chart(fig)

    dataframe3 = pd.read_excel('reports/air_forecasting/date_quantity.xlsx')
    dataframe4 = pd.read_excel('reports/air_raw_data/date_quantity.xlsx')

    # Display dataframes
    st.title("Quantity Analysis")


    # Merge dataframes
    merged_df = pd.concat([dataframe3, dataframe4], ignore_index=True)

    # Convert 'date' column to datetime format
    merged_df['date'] = pd.to_datetime(merged_df['date'])

    # Add IsFuture column
    merged_df['IsFuture'] = merged_df['date'] > pd.Timestamp.now()

    # Create plot
    fig = px.line(merged_df, x='date', y='data', title='Date Quantity Analysis', width=1000, color='IsFuture',
                color_discrete_map={True: 'green', False: 'blue'})
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Quantity')

    # Show plot
    st.plotly_chart(fig)

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
