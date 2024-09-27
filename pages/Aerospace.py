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

    with st.sidebar.expander("Sea Report ⛴"):
         st.page_link("Home.py", label="Sea Profit Monthly 📊")
    with st.sidebar.expander("Air Report ✈️"):
         st.page_link("pages/Airreport.py", label="Air Profit Monthly 📊")
    with st.sidebar.expander("Road Report 🛣️"):
         st.page_link("pages/Roadreport.py", label="Road Profit Monthly 📊")
    with st.sidebar.expander("Proje Report 🛣️"):
         st.page_link("pages/Proje.py", label="Proje Profit Monthly 📊")
    with st.sidebar.expander("Aerospace Report 🛣️"):
         st.page_link("pages/Aerospace.py", label="Aerospace Profit Monthly 📊")

    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout("Logout", "sidebar")

    # MongoDB connection string
    mongo_uri = "mongodb+srv://kkuseyri:GTTest2024@clusterv0.uwkchdi.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(mongo_uri)
    
    # Define the collection options
    collection_options = ["export_air", "export_land", "export_sea", "import_air", "import_land", "import_sea"]
    
    # Create a selectbox for the collection names
    selected_collection = st.selectbox("Select a Collection", collection_options, index=0)
    
    # Access the selected collection
    collection = client["GenelExportImport"][selected_collection]
    
    # Original branch list with lowercase values for logic
    branches = ["total", "istanbul", "izmir", "mersin"]
    
    # Create a new list for display purposes with uppercase first letters
    display_branches = [branch.title() for branch in branches]
    
    # Use the display_branches in the selectbox but retrieve the corresponding value from the original list
    selected_display_branch = st.selectbox("Select a Branch", display_branches, index=0)
    
    # Map the selected display branch back to the original branch value (lowercase)
    selected_branch = branches[display_branches.index(selected_display_branch)]
    
    # Modify the query based on selected branch
    branch_filter = {}  # Default, no filter for "Total"
    if selected_branch != "total":
        branch_filter = {"branch": selected_branch}

    # Fetch data from the selected collection with the filter
    data = list(collection.find(branch_filter))
    
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
    
    # Create DataFrames for the selected collection data
    if data:  # Ensure data exists
        combined_df = create_combined_df(data[0])
    
    # Display the combined HTML table in Streamlit
    if st.session_state["name"] == "Kerem Kuseyri" or st.session_state["name"] == "Üveys Aydemir" or st.session_state["name"] == "Kubilay Cebeci" or st.session_state["name"] == "Senem Çelik":
        if data:
            # Convert the DataFrame to HTML and display it
            st.dataframe(combined_df)  # Display the DataFrame as a table
        else:
            st.warning(f"No data found for branch: {selected_branch}")
    else:
        st.error("You are not eligible to see this page.")

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
    st.session_state.clear()  # Clears the entire session state
    st.session_state["rerun_trigger"] = True

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    st.session_state.clear()  # Clears the entire session state
    st.session_state["rerun_trigger"] = True
