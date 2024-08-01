import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import openpyxl
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

    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout("Logout", "sidebar")

    filenames = os.listdir('reports/air_export_employee_kpis')
    filenames.remove('count_per.xlsx')
    filenames.remove('price_weigth_per.xlsx')
    filenames_selected=st.selectbox("Select an employee", options= [name[:-5] for name in filenames], index=0)
    dataframe5 = pd.read_excel(f'reports/air_export_employee_kpis/'+ filenames_selected+ ".xlsx" )
    df5 = pd.DataFrame(dataframe5)
    

    dataframe1 = pd.read_excel('reports/air_export_employee_kpis/count_per.xlsx')
    df = pd.DataFrame(dataframe1)

    dataframe3 = pd.read_excel('reports/air_forecasting/date_quantity.xlsx')
    df3 = pd.DataFrame(dataframe3)

    dataframe2 = pd.read_excel('reports/air_export_employee_kpis/'+ filenames_selected+ ".xlsx")
    df2 = pd.DataFrame(dataframe2)

    dataframe4 = pd.read_excel('reports/air_import_employee_kpis/Aleyna BASAR.xlsx')
    df4 = pd.DataFrame(dataframe4)

    Export_Mean=df2["all_count_mean"][0]
    Import_Mean=df4["all_count_mean"][0]
    Total_Mean= Export_Mean + Import_Mean 
    Export_Percent=Export_Mean/Total_Mean
    Import_Percent=Import_Mean/Total_Mean

    Export_Forecast = df3["data"][0]*Export_Percent
    Import_Forecast = df3["data"][0]*Import_Percent
 
    column_sum=df['count'].sum()    
    specific_value = df.loc[df['employee_name'] == filenames_selected.split('.')[0], 'count'].values[0]
    contribution=specific_value/column_sum


    data = {'date': [datetime.now()], 'count': '60'} #df5['count'].iloc[-1]
    df6 = pd.DataFrame(data)

    fig = px.bar(df6, y='count', x='date', title=filenames_selected.split('.')[0],height=700, width=500,opacity=0.3)
    fig.update_xaxes(ticktext=[], tickvals=[1])
    fig.add_hline(y=df2["all_count_mean"][0], line_dash='dash', line_color='red', annotation_text=f'All Count Mean Value')
    fig.add_hline(y=Export_Forecast*contribution, line_dash='dash', line_color='orange', annotation_text=f'Prediction Target')
    fig.add_hline(y=Export_Forecast/4, line_dash='dash', line_color='purple', annotation_text=f'Count Per Employee Target')

    st.markdown("<br><br>",unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<br><br>",unsafe_allow_html=True)
    col1,col2=st.columns(2,gap="large")
    with col1:
        st.plotly_chart(fig)
        st.markdown(datetime.now().strftime("%Y-%m-%d"))
    with col2:

        st.write("<h1 style='font-size: 28px;'>Prediction Target:</h1>",unsafe_allow_html=True)
        st.warning(round((Export_Forecast*contribution),1))

        st.write("<h1 style='font-size: 28px;'>Count Per Employee Target:</h1>",unsafe_allow_html=True)
        st.info(round((Export_Forecast/4),1))
        st.write("<h1 style='font-size: 28px;'>All Count Mean:</h1>",unsafe_allow_html=True)
        st.error(round(df2["all_count_mean"][0],1))
    


elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


