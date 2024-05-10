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
    with st.sidebar.expander("Air Customer Report ✈️"):
        st.page_link("pages/Clientanalitics.py",label="Client Offer/Success Analysis", icon="📈")
        st.page_link("pages/Clientaircustomer.py",label="Client Air Customer Offer Analysis", icon="📈")
    

    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout("Logout", "sidebar")


    dataframe1 = pd.read_excel('reports/sea_forecasting/date_quantity.xlsx')
    dataframe2 = pd.read_excel('reports/sea_raw_data/date_quantity.xlsx')

    # Merge dataframes
    merged_df = pd.concat([dataframe2, dataframe1])
    merged_df['data'] = [round(float(data), 2) for data in merged_df['data']]
    # Convert 'date' column to datetime format
    merged_df['date'] = pd.to_datetime(merged_df['date'])

    # Add IsFuture column
    merged_df['IsFuture'] = merged_df['date'] > pd.Timestamp.now()

    # Define color function based on IsFuture column
    def get_color(is_future):
        return 'green' if is_future else 'blue'

    # Prepare series data
    seriesData = [
        {"time": int(time.timestamp()), "value": value, "color": get_color(is_future)}
        for time, value, is_future in zip(merged_df['date'], merged_df['data'], merged_df['IsFuture'])
    ]

    # Chart options
    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        }
    }

    # Series data for the chart
    seriesBaselineChart = [{
        "type": 'Line',
        "data": seriesData,
        "options": {
            "lineColor": 'rgba(0, 0, 0, 0)',  # Set initial line color as transparent
            "lineWidth": 2,
            "topLineColor": 'green',  # Color for future data
            "bottomLineColor": 'blue',  # Color for historical data
            "topFillColor1": 'green',  # Fill color for future data
            "topFillColor2": 'green',  # Fill color for future data
            "bottomFillColor1": 'blue',  # Fill color for historical data
            "bottomFillColor2": 'blue'  # Fill color for historical data
        }
    }]

    # Render the chart
    st.title("Sea Data Analysis")
    col1, col2= st.columns(2)
    with col1:
        st.info("Historical Data")
    with col2:
        st.success("Prediction")
    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesBaselineChart
        }
    ], 'sea_data_chart')



    dataframe1 = pd.read_excel('reports/sea_forecasting/date_teu.xlsx')
    dataframe2 = pd.read_excel('reports/sea_raw_data/date_teu.xlsx')

    # Display dataframes
    st.title("Sea TEU Analysis")
    col1, col2= st.columns(2)
    with col1:
        st.info("Historical Data")
    with col2:
        st.success("Prediction")

     # Merge dataframes
    merged_df = pd.concat([dataframe2, dataframe1])
    merged_df['data'] = [round(float(data), 2) for data in merged_df['data']]
    # Convert 'date' column to datetime format
    merged_df['date'] = pd.to_datetime(merged_df['date'])

    # Add IsFuture column
    merged_df['IsFuture'] = merged_df['date'] > pd.Timestamp.now()

    # Prepare series data
    seriesData = [
        {"time": int(time.timestamp()), "value": value, "color": get_color(is_future)}
        for time, value, is_future in zip(merged_df['date'], merged_df['data'], merged_df['IsFuture'])
    ]

    # Chart options
    chartOptions = {
        "layout": {
            "textColor": 'black',
            "background": {
                "type": 'solid',
                "color": 'white'
            }
        }
    }

    # Series data for the chart
    seriesBaselineChart = [{
        "type": 'Line',
        "data": seriesData,
        "options": {
            "lineColor": 'rgba(0, 0, 0, 0)',  # Set initial line color as transparent
            "lineWidth": 2,
            "topLineColor": 'green',  # Color for future data
            "bottomLineColor": 'blue',  # Color for historical data
            "topFillColor1": 'green',  # Fill color for future data
            "topFillColor2": 'green',  # Fill color for future data
            "bottomFillColor1": 'blue',  # Fill color for historical data
            "bottomFillColor2": 'blue'  # Fill color for historical data
        }
    }]



    renderLightweightCharts([
        {
            "chart": chartOptions,
            "series": seriesBaselineChart
        }
    ], 'sea_teu_chart')
    tab1, tab2 = st.tabs(["Shipment Count🔢", "Teu📦"])
    

    with tab1:



        # Read data from Excel file
        
        df = pd.read_excel('reports/sea_raw_data/quantity.xlsx')

       
        df['date'] = pd.to_datetime(df['date'])

        # Define min and max dates
        min_date = df['date'].min()
        max_date = df['date'].max()

        # Set default start and end dates within the min-max range
        default_start_date = min_date
        default_end_date = max_date

        # Filter data by date using a Streamlit date_input
        start_date = st.date_input('Select start date', min_value=min_date, max_value=max_date, value=default_start_date)
        end_date = st.date_input('Select end date', min_value=min_date, max_value=max_date, value=default_end_date)

        # Convert start_date and end_date to datetime64 dtype
        start_date = np.datetime64(start_date)
        end_date = np.datetime64(end_date)

        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
        df['date'] = df['date'].dt.strftime('%Y-%m')
        # Initialize table_data as an empty list
        table_data = []

        # Iterate over rows in the DataFrame
        for index, row in df.iterrows():
            date = (row['date'])
            city_values = {
                'A': {'E': 0, 'I': 0, 'T': 0},
                'B': {'E': 0, 'I': 0, 'T': 0},
                'FRW': {'E': 0, 'I': 0, 'T': 0}
            }
            city_values[row['bussnies_name']][row['direction']] = row['data']

            # Create row dictionary
            row_data = {
                'Date':date,
                'City': row['city_name'],
                'Data Type': 'data_count',
                'Export': f"A:{city_values['A']['E']} B:{city_values['B']['E']} FRW:{city_values['FRW']['E']}",
                'Import': f"A:{city_values['A']['I']} B:{city_values['B']['I']} FRW:{city_values['FRW']['I']}",
                'Cross Trade': f"A:{city_values['A']['T']} B:{city_values['B']['T']} FRW:{city_values['FRW']['T']}"
            }

            # Append row to table_data
            table_data.append(row_data)

        # Create DataFrame from table_data
        city_df = pd.DataFrame(table_data)

        # Display DataFrame using st.write




        # Group by date, city, and direction, summing the values
        grouped_df = df.groupby(['date', 'bussnies_name','city_name', 'direction']).sum().reset_index()

        # Initialize table_data as an empty list
        table_data = []

        # Iterate over rows in the grouped DataFrame
        for index, row in grouped_df.iterrows():
            date = row['date']
            city = row['city_name']
            bussiness_name = row['bussnies_name']
            direction = row['direction']
            value = row['data']

            # Create row dictionary
            row_data = {
                'Date': date,
                'City': city,
                'Branch': bussiness_name,
                'Export': 0,
                'Import': 0,
                'Cross Trade': 0
            }

            # Update row_data based on direction
            if direction == 'E':
                row_data['Export'] = value
            elif direction == 'I':
                row_data['Import'] = value
            elif direction == 'T':
                row_data['Cross Trade'] = value

            # Append row to table_data
            table_data.append(row_data)

        # Create DataFrame from table_data
        city_df = pd.DataFrame(table_data)

        # Combine rows with the same date and city
        combined_df = city_df.groupby(['Date', 'City','Branch']).sum().reset_index()

        # Display DataFrame using st.write




        # Group by date, city, branch, and direction, summing the values
        grouped_df = df.groupby(['date', 'bussnies_name', 'city_name', 'direction']).sum().reset_index()

        # Initialize table_data as an empty list
        table_data = []

        # Iterate over rows in the grouped DataFrame
        for index, row in grouped_df.iterrows():
            date = row['date']
            city = row['city_name']
            branch = row['bussnies_name']
            direction = row['direction']
            value = row['data']

            # Filter rows where branch is 'A'
            if branch == 'A':
                # Create row dictionary
                row_data = {
                    'Date': date,
                    'City': city,
                    'Branch': branch,
                    'Export': 0,
                    'Import': 0,
                    'Cross Trade': 0
                }

                # Update row_data based on direction
                if direction == 'E':
                    row_data['Export'] = value
                elif direction == 'I':
                    row_data['Import'] = value
                elif direction == 'T':
                    row_data['Cross Trade'] = value

                # Append row to table_data
                table_data.append(row_data)

        # Create DataFrame from table_data
        city_df = pd.DataFrame(table_data)

        # Combine rows with the same date, city, and branch
        combined_df = city_df.groupby(['Date', 'City', 'Branch']).sum().reset_index()

        # Display DataFrame using st.write

        st.header("Acenta:")
        st.write(combined_df)

        col1, col2, col3 = st.columns(3)

        grouped_data = city_df.groupby(['City', 'Date']).sum().reset_index()
        max_value = city_df[['Export', 'Import', 'Cross Trade']].astype(float).values.max()
        st.write(max_value)
        # Create figure and add bar chart trace
        fig = go.Figure()

        for city in grouped_data['City'].unique():
            city_data = grouped_data[grouped_data['City'] == city]
            fig.add_trace(go.Bar(
                x=city_data['Date'],
                y=city_data['Export'],
                name=city
            ))

        # Update layout
        fig.update_layout(
            title="Acenta Export",
            xaxis_title="Date",
            yaxis_title="Export",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col1:
            st.plotly_chart(fig, use_container_width=True, width=100, height=100)

        grouped_data_import = city_df.groupby(['City', 'Date']).sum().reset_index()

        # Create figure and add bar chart trace for Import data
        fig_import = go.Figure()

        for city in grouped_data_import['City'].unique():
            city_data_import = grouped_data_import[grouped_data_import['City'] == city]
            fig_import.add_trace(go.Bar(
                x=city_data_import['Date'],
                y=city_data_import['Import'],
                name=city
            ))

        # Update layout for Import plot
        fig_import.update_layout(
            title="Acenta Import",
            xaxis_title="Date",
            yaxis_title="Import",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col2:
            st.plotly_chart(fig_import, use_container_width=True, width=100, height=100)

        grouped_data_cross_trade = city_df.groupby(['City', 'Date']).sum().reset_index()

        # Create figure and add bar chart trace for Cross Trade data
        fig_cross_trade = go.Figure()

        for city in grouped_data_cross_trade['City'].unique():
            city_data_cross_trade = grouped_data_cross_trade[grouped_data_cross_trade['City'] == city]
            fig_cross_trade.add_trace(go.Bar(
                x=city_data_cross_trade['Date'],
                y=city_data_cross_trade['Cross Trade'],
                name=city
            ))

        # Update layout for Cross Trade plot
        fig_cross_trade.update_layout(
            title="Acenta Cross Trade",
            xaxis_title="Date",
            yaxis_title="Cross Trade",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col3:
            st.plotly_chart(fig_cross_trade, use_container_width=True, width=100, height=100)



        # Group by date, city, branch, and direction, summing the values
        grouped_df = df.groupby(['date', 'bussnies_name', 'city_name', 'direction']).sum().reset_index()

        # Initialize table_data as an empty list
        table_data = []

        # Iterate over rows in the grouped DataFrame
        for index, row in grouped_df.iterrows():
            date = row['date']
            city = row['city_name']
            branch = row['bussnies_name']
            direction = row['direction']
            value = row['data']

            # Filter rows where branch is 'B'
            if branch == 'B':
                # Create row dictionary
                row_data = {
                    'Date': date,
                    'City': city,
                    'Branch': branch,
                    'Export': 0,
                    'Import': 0,
                    'Cross Trade': 0
                }

                # Update row_data based on direction
                if direction == 'E':
                    row_data['Export'] = value
                elif direction == 'I':
                    row_data['Import'] = value
                elif direction == 'T':
                    row_data['Cross Trade'] = value

                # Append row to table_data
                table_data.append(row_data)

        # Create DataFrame from table_data
        city_df = pd.DataFrame(table_data)

        # Combine rows with the same date, city, and branch
        combined_df = city_df.groupby(['Date', 'City', 'Branch']).sum().reset_index()

        # Display DataFrame using st.write

        st.header("Bizim İşimiz:")
        st.write(combined_df)

        col1, col2, col3 = st.columns(3)

        grouped_data = city_df.groupby(['City', 'Date']).sum().reset_index()
        max_value = city_df[['Export', 'Import', 'Cross Trade']].astype(float).values.max()
        st.write(max_value)
        # Create figure and add bar chart trace
        fig = go.Figure()

        for city in grouped_data['City'].unique():
            city_data = grouped_data[grouped_data['City'] == city]
            fig.add_trace(go.Bar(
                x=city_data['Date'],
                y=city_data['Export'],
                name=city
            ))

        # Update layout
        fig.update_layout(
            title="Bizim İşimiz Export",
            xaxis_title="Date",
            yaxis_title="Export",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col1:
            st.plotly_chart(fig, use_container_width=True, width=100, height=100)

        grouped_data_import = city_df.groupby(['City', 'Date']).sum().reset_index()

        # Create figure and add bar chart trace for Import data
        fig_import = go.Figure()

        for city in grouped_data_import['City'].unique():
            city_data_import = grouped_data_import[grouped_data_import['City'] == city]
            fig_import.add_trace(go.Bar(
                x=city_data_import['Date'],
                y=city_data_import['Import'],
                name=city
            ))

        # Update layout for Import plot
        fig_import.update_layout(
            title="Bizim İşimiz Import",
            xaxis_title="Date",
            yaxis_title="Import",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col2:
            st.plotly_chart(fig_import, use_container_width=True, width=100, height=100)

        grouped_data_cross_trade = city_df.groupby(['City', 'Date']).sum().reset_index()

        # Create figure and add bar chart trace for Cross Trade data
        fig_cross_trade = go.Figure()

        for city in grouped_data_cross_trade['City'].unique():
            city_data_cross_trade = grouped_data_cross_trade[grouped_data_cross_trade['City'] == city]
            fig_cross_trade.add_trace(go.Bar(
                x=city_data_cross_trade['Date'],
                y=city_data_cross_trade['Cross Trade'],
                name=city
            ))

        # Update layout for Cross Trade plot
        fig_cross_trade.update_layout(
            title="Bizim İşimiz Cross Trade",
            xaxis_title="Date",
            yaxis_title="Cross Trade",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col3:
            st.plotly_chart(fig_cross_trade, use_container_width=True, width=100, height=100)




        # Group by date, city, and direction, summing the values
        grouped_df = df.groupby(['date', 'city_name', 'direction']).sum().reset_index()

        # Initialize table_data as an empty list
        table_data = []

        # Iterate over rows in the grouped DataFrame
        for index, row in grouped_df.iterrows():
            date = row['date']
            city = row['city_name']
            direction = row['direction']
            value = row['data']

            # Create row dictionary
            row_data = {
                'Date': date,
                'City': city,
                'Export': 0,
                'Import': 0,
                'Cross Trade': 0
            }

            # Update row_data based on direction
            if direction == 'E':
                row_data['Export'] = value
            elif direction == 'I':
                row_data['Import'] = value
            elif direction == 'T':
                row_data['Cross Trade'] = value

            # Append row to table_data
            table_data.append(row_data)

        # Create DataFrame from table_data
        city_df = pd.DataFrame(table_data)

        # Combine rows with the same date and city
        combined_df = city_df.groupby(['Date', 'City']).sum().reset_index()

        # Display DataFrame using st.write

        st.header("SUM:")
        st.write(combined_df)

        col1, col2, col3 = st.columns(3)

        grouped_data = city_df.groupby(['City', 'Date']).sum().reset_index()
        max_value = city_df[['Export', 'Import', 'Cross Trade']].astype(float).values.max()
        st.write(max_value)
        # Create figure and add bar chart trace
        fig = go.Figure()

        for city in grouped_data['City'].unique():
            city_data = grouped_data[grouped_data['City'] == city]
            fig.add_trace(go.Bar(
                x=city_data['Date'],
                y=city_data['Export'],
                name=city
            ))

        # Update layout
        fig.update_layout(
            title="Total Export",
            xaxis_title="Date",
            yaxis_title="Export",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col1:
            st.plotly_chart(fig, use_container_width=True, width=100, height=100)

        grouped_data_import = city_df.groupby(['City', 'Date']).sum().reset_index()

        # Create figure and add bar chart trace for Import data
        fig_import = go.Figure()

        for city in grouped_data_import['City'].unique():
            city_data_import = grouped_data_import[grouped_data_import['City'] == city]
            fig_import.add_trace(go.Bar(
                x=city_data_import['Date'],
                y=city_data_import['Import'],
                name=city
            ))

        # Update layout for Import plot
        fig_import.update_layout(
            title="Total Import",
            xaxis_title="Date",
            yaxis_title="Import",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col2:
            st.plotly_chart(fig_import, use_container_width=True, width=100, height=100)

        grouped_data_cross_trade = city_df.groupby(['City', 'Date']).sum().reset_index()

        # Create figure and add bar chart trace for Cross Trade data
        fig_cross_trade = go.Figure()

        for city in grouped_data_cross_trade['City'].unique():
            city_data_cross_trade = grouped_data_cross_trade[grouped_data_cross_trade['City'] == city]
            fig_cross_trade.add_trace(go.Bar(
                x=city_data_cross_trade['Date'],
                y=city_data_cross_trade['Cross Trade'],
                name=city
            ))

        # Update layout for Cross Trade plot
        fig_cross_trade.update_layout(
            title="Total Cross Trade",
            xaxis_title="Date",
            yaxis_title="Cross Trade",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col3:
            st.plotly_chart(fig_cross_trade, use_container_width=True, width=100, height=100)

            # Create figure and add line chart trace
        fig = px.line(grouped_data,markers=True, x='Date', y='Export', color='City', labels={'Export': 'Export Quantity'})
        fig.update_layout(
            title="Total Export",
            xaxis_title="Date",
            yaxis_title="Export",
        )
        with col1:
            st.plotly_chart(fig, use_container_width=True)

        # Repeat the same process for Import and Cross Trade plots

        fig_import = px.line(grouped_data_import,markers=True, x='Date', y='Import', color='City', labels={'Import': 'Import Quantity'})
        fig_import.update_layout(
            title="Total Import",
            xaxis_title="Date",
            yaxis_title="Import",
        )
        with col2:
            st.plotly_chart(fig_import, use_container_width=True)

        fig_cross_trade = px.line(grouped_data_cross_trade,markers=True, x='Date', y='Cross Trade', color='City', labels={'Cross Trade': 'Cross Trade Quantity'})
        fig_cross_trade.update_layout(
            title="Total Cross Trade",
            xaxis_title="Date",
            yaxis_title="Cross Trade",
        )
        with col3:
            st.plotly_chart(fig_cross_trade, use_container_width=True)

    with tab2:
        # Read data from Excel file
        
        df = pd.read_excel('reports/sea_raw_data/teu.xlsx')

        df['date'] = pd.to_datetime(df['date'])

        # Define min and max dates
        min_date = df['date'].min()
        max_date = df['date'].max()

        # Set default start and end dates within the min-max range
        default_start_date = min_date
        default_end_date = max_date

        # Filter data by date using a Streamlit slider
        start_date = st.date_input('Select start date', min_value=min_date, max_value=max_date, value=default_start_date,key='teu1')
        end_date = st.date_input('Select end date', min_value=min_date, max_value=max_date, value=default_end_date,key='teu2')

        # Convert start_date and end_date to datetime64 dtype
        start_date = np.datetime64(start_date)
        end_date = np.datetime64(end_date)

        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        
        df['date'] = df['date'].dt.strftime('%Y-%m')
        # Initialize table_data as an empty list
        table_data = []

        # Iterate over rows in the DataFrame
        for index, row in df.iterrows():
            date = (row['date'])
            city_values = {
                'A': {'E': 0, 'I': 0, 'T': 0},
                'B': {'E': 0, 'I': 0, 'T': 0},
                'FRW': {'E': 0, 'I': 0, 'T': 0}
            }
            city_values[row['bussnies_name']][row['direction']] = row['data']

            # Create row dictionary
            row_data = {
                'Date':date,
                'City': row['city_name'],
                'Data Type': 'data_count',
                'Export': f"A:{city_values['A']['E']} B:{city_values['B']['E']} FRW:{city_values['FRW']['E']}",
                'Import': f"A:{city_values['A']['I']} B:{city_values['B']['I']} FRW:{city_values['FRW']['I']}",
                'Cross Trade': f"A:{city_values['A']['T']} B:{city_values['B']['T']} FRW:{city_values['FRW']['T']}"
            }

            # Append row to table_data
            table_data.append(row_data)

        # Create DataFrame from table_data
        city_df = pd.DataFrame(table_data)

        # Display DataFrame using st.write




        # Group by date, city, and direction, summing the values
        grouped_df = df.groupby(['date', 'bussnies_name','city_name', 'direction']).sum().reset_index()

        # Initialize table_data as an empty list
        table_data = []

        # Iterate over rows in the grouped DataFrame
        for index, row in grouped_df.iterrows():
            date = row['date']
            city = row['city_name']
            bussiness_name = row['bussnies_name']
            direction = row['direction']
            value = row['data']

            # Create row dictionary
            row_data = {
                'Date': date,
                'City': city,
                'Branch': bussiness_name,
                'Export': 0,
                'Import': 0,
                'Cross Trade': 0
            }

            # Update row_data based on direction
            if direction == 'E':
                row_data['Export'] = value
            elif direction == 'I':
                row_data['Import'] = value
            elif direction == 'T':
                row_data['Cross Trade'] = value

            # Append row to table_data
            table_data.append(row_data)

        # Create DataFrame from table_data
        city_df = pd.DataFrame(table_data)

        # Combine rows with the same date and city
        combined_df = city_df.groupby(['Date', 'City','Branch']).sum().reset_index()

        # Display DataFrame using st.write




        # Group by date, city, branch, and direction, summing the values
        grouped_df = df.groupby(['date', 'bussnies_name', 'city_name', 'direction']).sum().reset_index()

        # Initialize table_data as an empty list
        table_data = []

        # Iterate over rows in the grouped DataFrame
        for index, row in grouped_df.iterrows():
            date = row['date']
            city = row['city_name']
            branch = row['bussnies_name']
            direction = row['direction']
            value = row['data']

            # Filter rows where branch is 'A'
            if branch == 'A':
                # Create row dictionary
                row_data = {
                    'Date': date,
                    'City': city,
                    'Branch': branch,
                    'Export': 0,
                    'Import': 0,
                    'Cross Trade': 0
                }

                # Update row_data based on direction
                if direction == 'E':
                    row_data['Export'] = value
                elif direction == 'I':
                    row_data['Import'] = value
                elif direction == 'T':
                    row_data['Cross Trade'] = value

                # Append row to table_data
                table_data.append(row_data)

        # Create DataFrame from table_data
        city_df = pd.DataFrame(table_data)

        # Combine rows with the same date, city, and branch
        combined_df = city_df.groupby(['Date', 'City', 'Branch']).sum().reset_index()

        # Display DataFrame using st.write

        st.header("Acenta:")
        st.write(combined_df)

        col1, col2, col3 = st.columns(3)

        grouped_data = city_df.groupby(['City', 'Date']).sum().reset_index()
        max_value = city_df[['Export', 'Import', 'Cross Trade']].astype(float).values.max()
        st.write(max_value)
        # Create figure and add bar chart trace
        fig = go.Figure()

        for city in grouped_data['City'].unique():
            city_data = grouped_data[grouped_data['City'] == city]
            fig.add_trace(go.Bar(
                x=city_data['Date'],
                y=city_data['Export'],
                name=city
            ))

        # Update layout
        fig.update_layout(
            title="Acenta Export",
            xaxis_title="Date",
            yaxis_title="Export",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col1:
            st.plotly_chart(fig, use_container_width=True, width=100, height=100)

        grouped_data_import = city_df.groupby(['City', 'Date']).sum().reset_index()

        # Create figure and add bar chart trace for Import data
        fig_import = go.Figure()

        for city in grouped_data_import['City'].unique():
            city_data_import = grouped_data_import[grouped_data_import['City'] == city]
            fig_import.add_trace(go.Bar(
                x=city_data_import['Date'],
                y=city_data_import['Import'],
                name=city
            ))

        # Update layout for Import plot
        fig_import.update_layout(
            title="Acenta Import",
            xaxis_title="Date",
            yaxis_title="Import",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col2:
            st.plotly_chart(fig_import, use_container_width=True, width=100, height=100)

        grouped_data_cross_trade = city_df.groupby(['City', 'Date']).sum().reset_index()

        # Create figure and add bar chart trace for Cross Trade data
        fig_cross_trade = go.Figure()

        for city in grouped_data_cross_trade['City'].unique():
            city_data_cross_trade = grouped_data_cross_trade[grouped_data_cross_trade['City'] == city]
            fig_cross_trade.add_trace(go.Bar(
                x=city_data_cross_trade['Date'],
                y=city_data_cross_trade['Cross Trade'],
                name=city
            ))

        # Update layout for Cross Trade plot
        fig_cross_trade.update_layout(
            title="Acenta Cross Trade",
            xaxis_title="Date",
            yaxis_title="Cross Trade",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col3:
            st.plotly_chart(fig_cross_trade, use_container_width=True, width=100, height=100)



        # Group by date, city, branch, and direction, summing the values
        grouped_df = df.groupby(['date', 'bussnies_name', 'city_name', 'direction']).sum().reset_index()

        # Initialize table_data as an empty list
        table_data = []

        # Iterate over rows in the grouped DataFrame
        for index, row in grouped_df.iterrows():
            date = row['date']
            city = row['city_name']
            branch = row['bussnies_name']
            direction = row['direction']
            value = row['data']

            # Filter rows where branch is 'B'
            if branch == 'B':
                # Create row dictionary
                row_data = {
                    'Date': date,
                    'City': city,
                    'Branch': branch,
                    'Export': 0,
                    'Import': 0,
                    'Cross Trade': 0
                }

                # Update row_data based on direction
                if direction == 'E':
                    row_data['Export'] = value
                elif direction == 'I':
                    row_data['Import'] = value
                elif direction == 'T':
                    row_data['Cross Trade'] = value

                # Append row to table_data
                table_data.append(row_data)

        # Create DataFrame from table_data
        city_df = pd.DataFrame(table_data)

        # Combine rows with the same date, city, and branch
        combined_df = city_df.groupby(['Date', 'City', 'Branch']).sum().reset_index()

        # Display DataFrame using st.write

        st.header("Bizim İşimiz:")
        st.write(combined_df)

        col1, col2, col3 = st.columns(3)

        grouped_data = city_df.groupby(['City', 'Date']).sum().reset_index()
        max_value = city_df[['Export', 'Import', 'Cross Trade']].astype(float).values.max()
        st.write(max_value)
        # Create figure and add bar chart trace
        fig = go.Figure()

        for city in grouped_data['City'].unique():
            city_data = grouped_data[grouped_data['City'] == city]
            fig.add_trace(go.Bar(
                x=city_data['Date'],
                y=city_data['Export'],
                name=city
            ))

        # Update layout
        fig.update_layout(
            title="Bizim İşimiz Export",
            xaxis_title="Date",
            yaxis_title="Export",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col1:
            st.plotly_chart(fig, use_container_width=True, width=100, height=100)

        grouped_data_import = city_df.groupby(['City', 'Date']).sum().reset_index()

        # Create figure and add bar chart trace for Import data
        fig_import = go.Figure()

        for city in grouped_data_import['City'].unique():
            city_data_import = grouped_data_import[grouped_data_import['City'] == city]
            fig_import.add_trace(go.Bar(
                x=city_data_import['Date'],
                y=city_data_import['Import'],
                name=city
            ))

        # Update layout for Import plot
        fig_import.update_layout(
            title="Bizim İşimiz Import",
            xaxis_title="Date",
            yaxis_title="Import",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col2:
            st.plotly_chart(fig_import, use_container_width=True, width=100, height=100)

        grouped_data_cross_trade = city_df.groupby(['City', 'Date']).sum().reset_index()

        # Create figure and add bar chart trace for Cross Trade data
        fig_cross_trade = go.Figure()

        for city in grouped_data_cross_trade['City'].unique():
            city_data_cross_trade = grouped_data_cross_trade[grouped_data_cross_trade['City'] == city]
            fig_cross_trade.add_trace(go.Bar(
                x=city_data_cross_trade['Date'],
                y=city_data_cross_trade['Cross Trade'],
                name=city
            ))

        # Update layout for Cross Trade plot
        fig_cross_trade.update_layout(
            title="Bizim İşimiz Cross Trade",
            xaxis_title="Date",
            yaxis_title="Cross Trade",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col3:
            st.plotly_chart(fig_cross_trade, use_container_width=True, width=100, height=100)




        # Group by date, city, and direction, summing the values
        grouped_df = df.groupby(['date', 'city_name', 'direction']).sum().reset_index()

        # Initialize table_data as an empty list
        table_data = []

        # Iterate over rows in the grouped DataFrame
        for index, row in grouped_df.iterrows():
            date = row['date']
            city = row['city_name']
            direction = row['direction']
            value = row['data']

            # Create row dictionary
            row_data = {
                'Date': date,
                'City': city,
                'Export': 0,
                'Import': 0,
                'Cross Trade': 0
            }

            # Update row_data based on direction
            if direction == 'E':
                row_data['Export'] = value
            elif direction == 'I':
                row_data['Import'] = value
            elif direction == 'T':
                row_data['Cross Trade'] = value

            # Append row to table_data
            table_data.append(row_data)

        # Create DataFrame from table_data
        city_df = pd.DataFrame(table_data)

        # Combine rows with the same date and city
        combined_df = city_df.groupby(['Date', 'City']).sum().reset_index()

        # Display DataFrame using st.write

        st.header("SUM:")
        st.write(combined_df)

        col1, col2, col3 = st.columns(3)

        grouped_data = city_df.groupby(['City', 'Date']).sum().reset_index()
        max_value = city_df[['Export', 'Import', 'Cross Trade']].astype(float).values.max()
        st.write(max_value)
        # Create figure and add bar chart trace
        fig = go.Figure()

        for city in grouped_data['City'].unique():
            city_data = grouped_data[grouped_data['City'] == city]
            fig.add_trace(go.Bar(
                x=city_data['Date'],
                y=city_data['Export'],
                name=city
            ))

        # Update layout
        fig.update_layout(
            title="Total Export",
            xaxis_title="Date",
            yaxis_title="Export",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col1:
            st.plotly_chart(fig, use_container_width=True, width=100, height=100)

        grouped_data_import = city_df.groupby(['City', 'Date']).sum().reset_index()

        # Create figure and add bar chart trace for Import data
        fig_import = go.Figure()

        for city in grouped_data_import['City'].unique():
            city_data_import = grouped_data_import[grouped_data_import['City'] == city]
            fig_import.add_trace(go.Bar(
                x=city_data_import['Date'],
                y=city_data_import['Import'],
                name=city
            ))

        # Update layout for Import plot
        fig_import.update_layout(
            title="Total Import",
            xaxis_title="Date",
            yaxis_title="Import",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col2:
            st.plotly_chart(fig_import, use_container_width=True, width=100, height=100)

        grouped_data_cross_trade = city_df.groupby(['City', 'Date']).sum().reset_index()

        # Create figure and add bar chart trace for Cross Trade data
        fig_cross_trade = go.Figure()

        for city in grouped_data_cross_trade['City'].unique():
            city_data_cross_trade = grouped_data_cross_trade[grouped_data_cross_trade['City'] == city]
            fig_cross_trade.add_trace(go.Bar(
                x=city_data_cross_trade['Date'],
                y=city_data_cross_trade['Cross Trade'],
                name=city
            ))

        # Update layout for Cross Trade plot
        fig_cross_trade.update_layout(
            title="Total Cross Trade",
            xaxis_title="Date",
            yaxis_title="Cross Trade",
            barmode='group',
            yaxis=dict(range=[0, max_value])
        )

        with col3:
            st.plotly_chart(fig_cross_trade, use_container_width=True, width=100, height=100)


        # Create figure and add line chart trace
        fig = px.line(grouped_data,markers=True, x='Date', y='Export', color='City', labels={'Export': 'Export Quantity'})
        fig.update_layout(
            title="Total Export",
            xaxis_title="Date",
            yaxis_title="Export",
        )
        with col1:
            st.plotly_chart(fig, use_container_width=True)

        # Repeat the same process for Import and Cross Trade plots

        fig_import = px.line(grouped_data_import,markers=True, x='Date', y='Import', color='City', labels={'Import': 'Import Teu'})
        fig_import.update_layout(
            title="Total Import",
            xaxis_title="Date",
            yaxis_title="Import",
        )
        with col2:
            st.plotly_chart(fig_import, use_container_width=True)

        fig_cross_trade = px.line(grouped_data_cross_trade,markers=True, x='Date', y='Cross Trade', color='City', labels={'Cross Trade': 'Cross Trade Teu'})
        fig_cross_trade.update_layout(
            title="Total Cross Trade",
            xaxis_title="Date",
            yaxis_title="Cross Trade",
        )
        with col3:
            st.plotly_chart(fig_cross_trade, use_container_width=True)

        

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    
