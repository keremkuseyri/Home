import pandas as pd
from pymongo import MongoClient
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import os

# Set up Streamlit page configuration
st.set_page_config(page_title='Genel Transport', 
                   page_icon="https://www.geneltransport.com.tr/wp-content/uploads/2021/03/favicon.png", 
                   layout='wide')

st.image('https://www.geneltransport.com.tr/wp-content/uploads/2021/03/logo-color.png')

# Load authentication config
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Set up authentication
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()

# Authentication check
if st.session_state["authentication_status"]:

    # Sidebar with page navigation
    with st.sidebar.expander("Sea Trend Report ⛴"):
        st.page_link("Home.py", label="Total", icon="📊")
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
    with st.sidebar.expander("Sea Report 📊"):
        st.page_link("pages/testdb2.py", label="Sea Profit Monthly 📊")

    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout("Logout", "sidebar")

    # MongoDB connection string
    mongo_uri = "mongodb+srv://kkuseyri:GTTest2024@clusterv0.uwkchdi.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(mongo_uri)

    # Access the database and collections
    db = client["GTProductImpExp"]
    collection_import = db["Import"]
    collection_export = db["Export"]

    branches = ["total", "istanbul", "izmir", "mersin"]
    display_branches = [branch.title() for branch in branches]

    selected_display_branch = st.selectbox("Select a Branch", display_branches, index=0)
    selected_branch = branches[display_branches.index(selected_display_branch)]

    branch_filter = {}
    if selected_branch != "total":
        branch_filter = {"branch": selected_branch}

    import_data = list(collection_import.find(branch_filter))
    export_data = list(collection_export.find(branch_filter))

    # Function to create a DataFrame for a specific category (budget, actual, percentage) and time period
    def create_category_df(data, category):
        rows = []
        for month in ["January", "February", "March", "April", "May", "June", 
                      "July", "August", "September", "October", "November", "December"]:
            month_data = data.get(category, {}).get(month.lower(), {})
            budget = month_data.get("budget", 0)
            actual = month_data.get("actual", 0)
            percentage = month_data.get("percentage", 0)
            rows.extend([(month, 'Budget', budget), (month, 'Actual', actual), (month, '+/- %', f"{percentage}%")])

        for period in [("Q1", "quarter_1"), ("Q2", "quarter_2"), ("Q3", "quarter_3"), ("Q4", "quarter_4"), 
                       ("H1", "half_1"), ("H2", "half_2"), ("Year", "year")]:
            period_data = data.get(category, {}).get(period[1], {})
            budget = period_data.get("budget", 0)
            actual = period_data.get("actual", 0)
            percentage = period_data.get("percentage", 0)
            rows.extend([(period[0], 'Budget', budget), (period[0], 'Actual', actual), (period[0], '+/- %', f"{percentage}%")])

        return rows

    # Function to combine all categories into a single DataFrame
    def create_combined_df(data):
        revenue_ours = create_category_df(data.get("revenue", {}), "ours")
        revenue_agency = create_category_df(data.get("revenue", {}), "agency")
        revenue_total = create_category_df(data.get("revenue", {}), "total")

        profit_ours = create_category_df(data.get("profit", {}), "ours")
        profit_agency = create_category_df(data.get("profit", {}), "agency")
        profit_total = create_category_df(data.get("profit", {}), "total")

        cargo_ours = create_category_df(data.get("amount_of_cargo", {}), "ours")
        cargo_agency = create_category_df(data.get("amount_of_cargo", {}), "agency")
        cargo_total = create_category_df(data.get("amount_of_cargo", {}), "total")

        combined_data = []
        for r_ours, r_agency, r_total, p_ours, p_agency, p_total, c_ours, c_agency, c_total in zip(
            revenue_ours, revenue_agency, revenue_total,
            profit_ours, profit_agency, profit_total,
            cargo_ours, cargo_agency, cargo_total
        ):
            combined_data.append([r_ours[2], r_agency[2], r_total[2], 
                                  p_ours[2], p_agency[2], p_total[2], 
                                  c_ours[2], c_agency[2], c_total[2]])

        column_tuples = [
            ("Revenue", "Ours"), ("Revenue", "Agency"), ("Revenue", "Total"),
            ("Profit", "Ours"), ("Profit", "Agency"), ("Profit", "Total"),
            ("Cargo", "Ours"), ("Cargo", "Agency"), ("Cargo", "Total")
        ]
        columns = pd.MultiIndex.from_tuples(column_tuples, names=["Category", "Type"])

        row_tuples = [
            (month, status) for month in ["January", "February", "March", "April", "May", "June", 
                                          "July", "August", "September", "October", "November", "December", 
                                          "Q1", "Q2", "Q3", "Q4", "H1", "H2", "Year"]
            for status in ['Budget', 'Actual', '+/- %']
        ]
        rows = pd.MultiIndex.from_tuples(row_tuples, names=["Period", "Status"])

        df = pd.DataFrame(combined_data, columns=columns, index=rows)
        return df

    # Function to format the values (e.g. add commas for larger numbers)
   def format_value(value):
      try:
          print(f"Original value: {value} ({type(value)})")  # Debugging statement
          
          # Handle percentages as they are, assuming they're already formatted strings
          if isinstance(value, str) and '%' in value:
              return value
          
          # Check if value is a float or int and format accordingly
          elif isinstance(value, (int, float)):
              formatted_value = "{:,.0f}".format(value)  # Format numbers with commas and no decimal places
              print(f"Formatted value: {formatted_value}")  # Debugging statement
              return formatted_value
          
          # If value is something unexpected, return it as is
          else:
              return value
      except Exception as e:
            print(f"Error formatting value: {e}")  # Debugging statement
            return value

    # Function to create an HTML table to display the data
    def create_html_table(df_import, df_export):
        html = "<table border='1' style='border-collapse: collapse; width: 100%;'>"

        html += "<thead><tr>"
        html += "<th rowspan='3' style='text-align: center; font-weight: normal;'></th>"
        html += "<th rowspan='3' style='text-align: center; font-weight: normal;'></th>"
        html += "<th colspan='9' style='text-align: center; background-color: #EEFC5E;'>Export</th>"
        html += "<th colspan='9' style='text-align: center; background-color: #EEFC5E;'>Import</th>"
        html += "</tr>"

        html += "<tr>"
        for _ in range(2):
            html += "<th colspan='3' style='text-align: center; background-color: #F4CCCC;'>Revenue</th>"
            html += "<th colspan='3' style='text-align: center; background-color: #D0E0E3;'>Profit</th>"
            html += "<th colspan='3' style='text-align: center; background-color: #D9EAD3;'>Cargo</th>"
        html += "</tr>"

        html += "<tr>"
        for _ in range(2):
            html += "<th style='text-align: center;'>Ours</th>"
            html += "<th style='text-align: center;'>Agency</th>"
            html += "<th style='text-align: center;'>Total</th>"
        html += "</tr></thead>"

        html += "<tbody>"
        for row_label, row_data_export, row_data_import in zip(df_export.index, df_export.values, df_import.values):
            html += f"<tr><td colspan='2' style='text-align: center;'>{row_label[0]}</td>"

            for value in row_data_export:
                html += f"<td style='text-align: center; background-color: #FFF2CC;'>{format_value(value)}</td>"
            for value in row_data_import:
                html += f"<td style='text-align: center; background-color: #D9EAD3;'>{format_value(value)}</td>"

            html += "</tr>"
        html += "</tbody></table>"
        return html

    # Generate the DataFrame for import and export
    df_import = create_combined_df(import_data)
    df_export = create_combined_df(export_data)

    # Create the HTML table and display it
    html_table = create_html_table(df_import, df_export)
    st.markdown(html_table, unsafe_allow_html=True)

# If not authenticated
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

    # Clear the session state
    st.session_state.clear()

    # Set a trigger to rerun the app after session state is cleared
    st.session_state["rerun_trigger"] = True

else:
    st.error('Username/password is incorrect')
  
    # Clear the session state
    st.session_state.clear()

    # Set a trigger to rerun the app after session state is cleared
    st.session_state["rerun_trigger"] = True
