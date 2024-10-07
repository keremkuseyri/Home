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
    config['cookie']['expiry_days']
)

authenticator.login()
if st.session_state["authentication_status"]:
    


    with st.sidebar.expander("Sea Report ⛴"):
         st.page_link("pages/Home.py", label="Sea Profit Monthly 📊")
    with st.sidebar.expander("Air Report ✈️"):
         st.page_link("pages/Airreport.py", label="Air Profit Monthly 📊")
    with st.sidebar.expander("Road Report 🛣️"):
         st.page_link("pages/Roadreport.py", label="Road Profit Monthly 📊")

    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout("Logout", "sidebar")

    # MongoDB connection string
    mongo_uri = "mongodb+srv://kkuseyri:GTTest2024@clusterv0.uwkchdi.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(mongo_uri)
    
    # Access the database and collections
    db = client["GTProductImpExp"]
    collection_import = db["import_sea"]
    collection_export = db["export_sea"]
    
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

    # Fetch data from collections with the filter
    import_data = list(collection_import.find(branch_filter))
    export_data = list(collection_export.find(branch_filter))
    
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
    # Modified Function to create an HTML table with specified styling
    # Modified Function to create an HTML table with an additional header row

    
    def create_html_table(df_import, df_export):
        html = "<table border='1' style='border-collapse: collapse; width: 100%;'>"
        
        # Top header row for Export and Import
        html += "<thead><tr>"
        html += "<th rowspan='3' style='text-align: center; font-weight: normal;'></th>"
        html += "<th rowspan='3' style='text-align: center; font-weight: normal;'></th>"
        
        # Export header spanning its columns
        html += "<th colspan='9' style='text-align: center; background-color: #EEFC5E;'>Export</th>"
        
        # Import header spanning its columns
        html += "<th colspan='9' style='text-align: center; background-color: #EEFC5E;'>Import</th>"
        html += "</tr>"
        
        # Second header row for Revenue, Profit, Cargo under Export and Import
        html += "<tr>"
        for _ in range(2):  # Once for Export, once for Import
            html += "<th colspan='3' style='text-align: center; background-color: #F4CCCC;'>Revenue</th>"
            html += "<th colspan='3' style='text-align: center; background-color: #D0E0E3;'>Profit</th>"
            html += "<th colspan='3' style='text-align: center; background-color: #D9EAD3;'>Cargo</th>"
        html += "</tr>"
        
        # Third header row for Ours, Agency, Total under Revenue, Profit, Cargo
        html += "<tr>"
        for _ in range(2):  # Once for Export, once for Import
            html += "<th style='text-align: center;'>Ours</th>"
            html += "<th style='text-align: center;'>Agency</th>"
            html += "<th style='text-align: center;'>Total</th>"
            html += "<th style='text-align: center;'>Ours</th>"
            html += "<th style='text-align: center;'>Agency</th>"
            html += "<th style='text-align: center;'>Total</th>"
            html += "<th style='text-align: center;'>Ours</th>"
            html += "<th style='text-align: center;'>Agency</th>"
            html += "<th style='text-align: center;'>Total</th>"
        html += "</tr>"
        html += "</thead>"
        
        # Add the rows with merged cells
        html += "<tbody>"
        
        prev_period = None
        rowspan = 1
        for index in df_import.index:
            period, status = index
        
            # Skip H1 and H2 rows
            if period in ["H1", "H2"]:
                continue
        
            # If period changes, close the previous row's cell
            if period != prev_period:
                if prev_period is not None:
                    html = html.replace(f"ROWSPAN_{prev_period}", str(rowspan))
                rowspan = 1
                prev_period = period
                html += f"<tr><td rowspan='ROWSPAN_{period}' style='text-align: center; font-weight: bold;'>{period}</td><td style='text-align: center;'>{status}</td>"
            else:
                rowspan += 1
                html += f"<tr><td style='text-align: center;'>{status}</td>"
        
            # Function to format numbers or percentages
            def format_value(value):
                try:
                    # Check if the value contains a '%' symbol
                    if isinstance(value, str) and '%' in value:
                        return value  # Keep as is for percentage strings
                    else:
                        return f"{int(value):,}"  # Format numbers with commas
                except (ValueError, TypeError):
                    return value  # Return the value as is if it cannot be converted
    
            # Adding Export data
            revenue_export = df_export.loc[index, ('Revenue', 'Ours')], df_export.loc[index, ('Revenue', 'Agency')], df_export.loc[index, ('Revenue', 'Total')]
            profit_export = df_export.loc[index, ('Profit', 'Ours')], df_export.loc[index, ('Profit', 'Agency')], df_export.loc[index, ('Profit', 'Total')]
            cargo_export = df_export.loc[index, ('Cargo', 'Ours')], df_export.loc[index, ('Cargo', 'Agency')], df_export.loc[index, ('Cargo', 'Total')]
            
            for value in revenue_export:
                html += f"<td style='text-align: center; background-color: #F4CCCC;'>{format_value(value)}</td>"  # Pink for Revenue
            for value in profit_export:
                html += f"<td style='text-align: center; background-color: #D0E0E3;'>{format_value(value)}</td>"  # Blue for Profit
            for value in cargo_export:
                html += f"<td style='text-align: center; background-color: #D9EAD3;'>{format_value(value)}</td>"  # Green for Cargo
    
            # Adding Import data
            revenue_import = df_import.loc[index, ('Revenue', 'Ours')], df_import.loc[index, ('Revenue', 'Agency')], df_import.loc[index, ('Revenue', 'Total')]
            profit_import = df_import.loc[index, ('Profit', 'Ours')], df_import.loc[index, ('Profit', 'Agency')], df_import.loc[index, ('Profit', 'Total')]
            cargo_import = df_import.loc[index, ('Cargo', 'Ours')], df_import.loc[index, ('Cargo', 'Agency')], df_import.loc[index, ('Cargo', 'Total')]
            
            for value in revenue_import:
                html += f"<td style='text-align: center; background-color: #F4CCCC;'>{format_value(value)}</td>"  # Pink for Revenue
            for value in profit_import:
                html += f"<td style='text-align: center; background-color: #D0E0E3;'>{format_value(value)}</td>"  # Blue for Profit
            for value in cargo_import:
                html += f"<td style='text-align: center; background-color: #D9EAD3;'>{format_value(value)}</td>"  # Green for Cargo
        
            html += "</tr>"
        
        # Final replacement for the last period
        if prev_period is not None:
            html = html.replace(f"ROWSPAN_{prev_period}", str(rowspan))
        
        html += "</tbody>"
        html += "</table>"
        return html












    
    # Create DataFrames for Import and Export data with the filtered branch data
    if import_data:  # Ensure data exists
        import_combined_df = create_combined_df(import_data[0])
    if export_data:  # Ensure data exists
        export_combined_df = create_combined_df(export_data[0])
    
    # Display the combined HTML table in Streamlit
    if st.session_state["name"] == "Kerem Kuseyri" or st.session_state["name"] == "Üveys Aydemir" or st.session_state["name"] == "Kubilay Cebeci" or st.session_state["name"] == "Senem Çelik":
        if import_data and export_data:
                combined_html_table = create_html_table(import_combined_df, export_combined_df)
                st.markdown(combined_html_table, unsafe_allow_html=True)
        else:
                st.warning(f"No data found for branch: {selected_branch}")

    else :
         st.error("You are not eligible to see this page.")



elif st.session_state["authentication_status"] is False:


    st.error('Username/password is incorrect')
    st.session_state.clear()  # Clears the entire session state
    st.session_state["rerun_trigger"] = True

elif st.session_state["authentication_status"] is None:


    st.warning('Please enter your username and password')
    st.session_state.clear()  # Clears the entire session state
    st.session_state["rerun_trigger"] = True
