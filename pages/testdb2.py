import pandas as pd
from pymongo import MongoClient
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import os

# Set up Streamlit page configuration
st.set_page_config(page_title='Genel Transport', page_icon="https://www.geneltransport.com.tr/wp-content/uploads/2021/03/favicon.png", layout='wide')
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
        st.page_link("pages/Air.py", label="Total", icon="📊")
    with st.sidebar.expander("Air Export KPI 🎯"):
        st.page_link("pages/Airexportkpi.py", label="Air Export KPI", icon="📊")
        st.page_link("pages/Airexporttarget.py", label="Target Export KPI", icon="🎯")
    with st.sidebar.expander("Air Import KPI 🎯"):
        st.page_link("pages/Airimportkpi.py", label="Air Import KPI", icon="📊")
        st.page_link("pages/Airimporttarget.py", label="Target Import KPI", icon="🎯")
    with st.sidebar.expander("Air Customer Report ✈️"):
        st.page_link("pages/Clientanalitics.py", label="Client Offer/Success Analysis", icon="📈")
        st.page_link("pages/Clientaircustomer.py", label="Client Air Customer Offer Analysis", icon="📈")
    with st.sidebar.expander("Air Import/Export Yearly 📊"):
         st.page_link("pages/testdb2.py", label="Air Import/Export Yearly 📊")

    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout("Logout", "sidebar")

    # MongoDB connection string
    mongo_uri = "mongodb+srv://kkuseyri:GTTest2024@clusterv0.uwkchdi.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(mongo_uri)

    # Access the database and collections
    db = client["GTProductImpExp"]
    collection_import = db["Import"]
    collection_export = db["Export"]

    # Fetch data from collections
    import_data = list(collection_import.find({}))
    export_data = list(collection_export.find({}))

    # Function to create DataFrames for 'ours', 'agency', and 'total'
    def create_category_df(data, category):
        rows = []
        for month in ["January", "February", "March", "April", "May", "June", 
                      "July", "August", "September", "October", "November", "December"]:
            month_data = data.get(category, {}).get(month.lower(), {})
            budget = month_data.get("budget", 0)
            actual = month_data.get("actual", 0)
            percentage = month_data.get("percentage", 0)
            rows.extend([(month, 'Budget', budget), (month, 'Actual', actual), (month, '+/- %', f"{percentage}%")])

        # Adding quarterly, half-yearly, and yearly data
        for period in [("Q1", "quarter_1"), ("Q2", "quarter_2"), ("Q3", "quarter_3"), ("Q4", "quarter_4"), 
                       ("H1", "half_1"), ("H2", "half_2"), ("Year", "year")]:
            period_data = data.get(category, {}).get(period[1], {})
            budget = period_data.get("budget", 0)
            actual = period_data.get("actual", 0)
            percentage = period_data.get("percentage", 0)
            rows.extend([(period[0], 'Budget', budget), (period[0], 'Actual', actual), (period[0], '+/- %', f"{percentage}%")])

        return rows

    # Function to structure the data into a single DataFrame
    def create_combined_df(data):
        # Extracting the data for each category
        revenue_ours = create_category_df(data.get("revenue", {}), "ours")
        revenue_agency = create_category_df(data.get("revenue", {}), "agency")
        revenue_total = create_category_df(data.get("revenue", {}), "total")

        profit_ours = create_category_df(data.get("profit", {}), "ours")
        profit_agency = create_category_df(data.get("profit", {}), "agency")
        profit_total = create_category_df(data.get("profit", {}), "total")

        cargo_ours = create_category_df(data.get("amount_of_cargo", {}), "ours")
        cargo_agency = create_category_df(data.get("amount_of_cargo", {}), "agency")
        cargo_total = create_category_df(data.get("amount_of_cargo", {}), "total")

        # Combining the data
        combined_data = []
        for r_ours, r_agency, r_total, p_ours, p_agency, p_total, c_ours, c_agency, c_total in zip(
            revenue_ours, revenue_agency, revenue_total,
            profit_ours, profit_agency, profit_total,
            cargo_ours, cargo_agency, cargo_total
        ):
            combined_data.append([r_ours[2], r_agency[2], r_total[2], 
                                  p_ours[2], p_agency[2], p_total[2], 
                                  c_ours[2], c_agency[2], c_total[2]])

        # Define the multi-index for columns
        column_tuples = [
            ("Revenue", "Ours"), ("Revenue", "Agency"), ("Revenue", "Total"),
            ("Profit", "Ours"), ("Profit", "Agency"), ("Profit", "Total"),
            ("Cargo", "Ours"), ("Cargo", "Agency"), ("Cargo", "Total")
        ]
        columns = pd.MultiIndex.from_tuples(column_tuples, names=["Category", "Type"])

        # Define the multi-index for rows
        row_tuples = [
            (month, status) for month in ["January", "February", "March", "April", "May", "June", 
                                          "July", "August", "September", "October", "November", "December", 
                                          "Q1", "Q2", "Q3", "Q4", "H1", "H2", "Year"]
            for status in ['Budget', 'Actual', '+/- %']
        ]
        rows = pd.MultiIndex.from_tuples(row_tuples, names=["Period", "Status"])

        # Create the DataFrame
        df = pd.DataFrame(combined_data, columns=columns, index=rows)
        return df

    # Create DataFrames for Import and Export data
    import_combined_df = create_combined_df(import_data[0])
    export_combined_df = create_combined_df(export_data[0])

    # Function to create an HTML table with specified styling
    def create_html_table(df_import, df_export):
        html = "<table border='1' style='border-collapse: collapse; width: 100%;'>"
    
        # Top header row for Export and Import (switched)
        html += "<thead><tr>"
        html += "<th rowspan='3' style='text-align: center; font-weight: normal;'></th>"
        html += "<th rowspan='3' style='text-align: center; font-weight: normal;'></th>"
    
        # Export header spanning its columns (switched to the left)
        html += "<th colspan='9' style='text-align: center; background-color: #EEFC5E;'>Export</th>"
    
        # Import header spanning its columns (switched to the right)
        html += "<th colspan='9' style='text-align: center; background-color: #EEFC5E;'>Import</th>"
        html += "</tr>"
    
        # Second header row for Revenue, Profit, Cargo under Export and Import (switched)
        html += "<tr>"
        for _ in range(2):  # Once for Export, once for Import
            html += "<th colspan='3' style='text-align: center; background-color: #D9EAD3;'>Revenue</th>"
            html += "<th colspan='3' style='text-align: center; background-color: #D0E0E3;'>Profit</th>"
            html += "<th colspan='3' style='text-align: center; background-color: #F4CCCC;'>Cargo</th>"
        html += "</tr>"
    
        # Third header row for Ours, Agency, Total under Revenue, Profit, Cargo (switched positions)
        html += "<tr>"
        for _ in range(2):  # Once for Export, once for Import
            for category in ["Ours", "Agency", "Total"]:
                html += f"<th style='text-align: center;'>{category}</th>"
            for category in ["Ours", "Agency", "Total"]:
                html += f"<th style='text-align: center;'>{category}</th>"
        html += "</tr>"
        html += "</thead>"
    
        # Table body
        html += "<tbody>"
    
        # Iterate over DataFrame index (Period, Status)
        for index in df_import.index:
            html += "<tr>"
            html += f"<td>{index[0]}</td><td>{index[1]}</td>"
    
            # Adding Export Data (switched to appear before Import data)
            for category in df_export.columns.levels[0]:
                for type_ in df_export.columns.levels[1]:
                    # Convert float values to integers (leave percentages unchanged)
                    value = df_export.loc[index, (category, type_)]
                    if isinstance(value, (float, int)):  # If it's a number, convert to integer
                        value = int(value)
                    html += f"<td style='text-align: center;'>{value}</td>"
    
            # Adding Import Data (switched to appear after Export data)
            for category in df_import.columns.levels[0]:
                for type_ in df_import.columns.levels[1]:
                    # Convert float values to integers (leave percentages unchanged)
                    value = df_import.loc[index, (category, type_)]
                    if isinstance(value, (float, int)):  # If it's a number, convert to integer
                        value = int(value)
                    html += f"<td style='text-align: center;'>{value}</td>"
    
            html += "</tr>"
    
        html += "</tbody>"
        html += "</table>"
        return html


    # Generate HTML table from DataFrames
    html_table = create_html_table(import_combined_df, export_combined_df)

    # Display the HTML table using Streamlit
    st.markdown(html_table, unsafe_allow_html=True)

elif st.session_state["authentication_status"] == False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] == None:
    st.warning("Please enter your username and password")
