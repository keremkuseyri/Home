import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import openpyxl
import os

st.set_page_config(page_title='Genel Transport',page_icon="https://www.geneltransport.com.tr/wp-content/uploads/2021/03/favicon.png", layout='wide')
st.image('https://www.geneltransport.com.tr/wp-content/uploads/2021/03/logo-color.png')

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
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
    with st.sidebar.expander("Sea Report ⛴"):
         st.page_link("pages/testdb2.py", label="Sea Profit Monthly 📊")
    with st.sidebar.expander("Air Report ✈️"):
         st.page_link("pages/Airreport.py", label="Air Profit Monthly 📊")
    with st.sidebar.expander("Road Report 🛣️"):
         st.page_link("pages/Roadreport.py", label="Road Profit Monthly 📊")

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
    filenames = os.listdir('reports/air_import_employee_kpis')
    filenames.remove('count_per.xlsx')
    filenames.remove('price_weigth_per.xlsx')
    filenames_selected=st.selectbox("Select an employee", options= [name[:-5] for name in filenames], index=0)
    dataframe1 = pd.read_excel(f'reports/air_import_employee_kpis/'+ filenames_selected+'.xlsx')
    df = pd.DataFrame(dataframe1)
    st.write(dataframe1)
    fig = px.line(df,y='count', x='date', title='Employee Quantity to Date', width=1450)
    fig.add_hline(y=df["all_count_mean"][0], line_dash='3 5', line_color='green', annotation_text=f'All Count Mean Value')
    fig.add_hline(y=df["count_mean"][0], line_dash='3 5', line_color='orange', annotation_text=f'Count Mean')
    fig.add_hline(y=df["count_max"][0], line_dash='3 5', line_color='red', annotation_text=f'Count Max')
    fig.add_hline(y=df["count_min"][0], line_dash='3 5', line_color='purple', annotation_text=f'Count Min')

    st.plotly_chart(fig)

    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.info("All count mean:")
        st.success(round(df["all_count_mean"][0],1))
    with col2:
        st.info("Count Mean:")
        st.success(round(df["count_mean"][0],1))
    with col3:
        st.info("Count Max:")
        st.success(round(df["count_max"][0],1))
    with col4:
        st.info("Count Min:")
        st.success(round(df["count_min"][0],1))
    fig2= px.line(df,y='price_weigth', x='date', title='Employee Price-Weight Distribution', width=1450)
    fig2.add_hline(y=df["all_price_weigth_mean"][0], line_dash='3 5', line_color='green', annotation_text=f'All Price Weight Mean Value')
    fig2.add_hline(y=df["price_weigth_mean"][0], line_dash='3 5', line_color='orange', annotation_text=f'Price Weight Mean')
    fig2.add_hline(y=df["price_weigth_max"][0], line_dash='3 5', line_color='red', annotation_text=f'Price Weight Max')
    fig2.add_hline(y=df["price_weigth_min"][0], line_dash='3 5', line_color='purple', annotation_text=f'Price Weight Min')

    st.plotly_chart(fig2)
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.info("All Price Weight Mean Value:")
        st.success(round(df["all_price_weigth_mean"][0],1))
    with col2:
        st.info("Price Weight Mean:")
        st.success(round(df["price_weigth_mean"][0],1))
    with col3:
        st.info("Price Weight Max:")
        st.success(round(df["price_weigth_max"][0],1))
    with col4:
        st.info("Price Weight Min:")
        st.success(round(df["price_weigth_min"][0],1))

elif st.session_state["authentication_status"] is False:


    st.error('Username/password is incorrect')
    st.session_state.clear()  # Clears the entire session state
    st.session_state["rerun_trigger"] = True

elif st.session_state["authentication_status"] is None:


    st.warning('Please enter your username and password')
    st.session_state.clear()  # Clears the entire session state
    st.session_state["rerun_trigger"] = True
