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
         st.page_link("Home.py", label="Sea Profit Monthly 📊")
    with st.sidebar.expander("Air Report ✈️"):
         st.page_link("pages/Airreport.py", label="Air Profit Monthly 📊")
    with st.sidebar.expander("Road Report 🛣️"):
         st.page_link("pages/Roadreport.py", label="Road Profit Monthly 📊")
    with st.sidebar.expander("Project Report 📝"):
         st.page_link("pages/Project.py", label="Project Profit Monthly 📊")
    with st.sidebar.expander("Aerospace Report 🚀"):
         st.page_link("pages/Aerospace.py", label="Aerospace Profit Monthly 📊")
    with st.sidebar.expander("Sales General Format 💵"):
         st.page_link("pages/Generalformat.py", label="Sales General Format Monthly 📊")
    with st.sidebar.expander("Key Account 🔑"):
         st.page_link("pages/Keyaccount.py", label="Key Account Monthly 📊")

    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
    authenticator.logout("Logout", "sidebar")

    # MongoDB connection string
    mongo_uri = "mongodb+srv://kkuseyri:GTTest2024@clusterv0.uwkchdi.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(mongo_uri)
    
    # Access the database and collections
    db = client["GTProductImpExp"]
    collection_import = db["import_land"]
    collection_export = db["export_land"]
    
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
        
        # Top header row for Export, Import, and Total
        html += "<thead><tr>"
        html += "<th rowspan='3' style='text-align: center; font-weight: normal;'></th>"
        html += "<th rowspan='3' style='text-align: center; font-weight: normal;'></th>"
        
        # Export header spanning its columns
        html += "<th colspan='9' style='text-align: center; background-color: #EEFC5E;'>Export</th>"
        
        # Import header spanning its columns
        html += "<th colspan='9' style='text-align: center; background-color: #EEFC5E;'>Import</th>"
        
        # Total header spanning its columns
        html += "<th colspan='9' style='text-align: center; background-color: #EEFC5E;'>Total</th>"
        html += "</tr>"
        
        # Second header row for Revenue, Profit, Cargo under Export, Import, and Total
        html += "<tr>"
        for _ in range(3):  # Once for Export, Import, and Total
            html += "<th colspan='3' style='text-align: center; background-color: #F4CCCC;'>Revenue</th>"
            html += "<th colspan='3' style='text-align: center; background-color: #D0E0E3;'>Profit</th>"
            html += "<th colspan='3' style='text-align: center; background-color: #D9EAD3;'>Cargo</th>"
        html += "</tr>"
        
        # Third header row for Ours, Agency, Total under Revenue, Profit, Cargo
        html += "<tr>"
        for _ in range(3):  # Once for Export, Import, and Total
            # Ours, Agency, Total for Revenue
            html += "<th style='text-align: center;'>Ours</th>"
            html += "<th style='text-align: center;'>Agency</th>"
            html += "<th style='text-align: center;'>Total</th>"
        
            # Ours, Agency, Total for Profit
            html += "<th style='text-align: center;'>Ours</th>"
            html += "<th style='text-align: center;'>Agency</th>"
            html += "<th style='text-align: center;'>Total</th>"
        
            # Ours, Agency, Total for Cargo
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
                        return f"{int(value):,}".replace(",", ".")  # Format numbers with commas
                except (ValueError, TypeError):
                    return value  # Return the value as is if it cannot be converted
            
            # Function to handle percentages
            def calculate_percentage_mean(value1, value2):
                try:
                    # Remove the '%' symbol and convert to float
                    value1 = float(value1.replace('%', '')) if isinstance(value1, str) and '%' in value1 else float(value1)
                    value2 = float(value2.replace('%', '')) if isinstance(value2, str) and '%' in value2 else float(value2)
                    
                    # Calculate the mean and return as an integer percentage
                    return f"{int((value1 + value2) / 2)}%"  # Convert float to int and append '%'
                except (ValueError, TypeError):
                    return ""  # Return empty string if conversion fails

            
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

            # Adding Total data by summing Export and Import values
            total_revenue_ours = revenue_export[0] + revenue_import[0]
            total_revenue_agency = revenue_export[1] + revenue_import[1]
            total_revenue_total = revenue_export[2] + revenue_import[2]

            total_profit_ours = profit_export[0] + profit_import[0]
            total_profit_agency = profit_export[1] + profit_import[1]
            total_profit_total = profit_export[2] + profit_import[2]

            total_cargo_ours = cargo_export[0] + cargo_import[0]
            total_cargo_agency = cargo_export[1] + cargo_import[1]
            total_cargo_total = cargo_export[2] + cargo_import[2]
            
            # Check if any total value is a percentage and calculate the mean
            total_revenue_ours = calculate_percentage_mean(revenue_export[0], revenue_import[0]) if '%' in str(revenue_export[0]) or '%' in str(revenue_import[0]) else total_revenue_ours
            total_revenue_agency = calculate_percentage_mean(revenue_export[1], revenue_import[1]) if '%' in str(revenue_export[1]) or '%' in str(revenue_import[1]) else total_revenue_agency
            total_revenue_total = calculate_percentage_mean(revenue_export[2], revenue_import[2]) if '%' in str(revenue_export[2]) or '%' in str(revenue_import[2]) else total_revenue_total

            total_profit_ours = calculate_percentage_mean(profit_export[0], profit_import[0]) if '%' in str(profit_export[0]) or '%' in str(profit_import[0]) else total_profit_ours
            total_profit_agency = calculate_percentage_mean(profit_export[1], profit_import[1]) if '%' in str(profit_export[1]) or '%' in str(profit_import[1]) else total_profit_agency
            total_profit_total = calculate_percentage_mean(profit_export[2], profit_import[2]) if '%' in str(profit_export[2]) or '%' in str(profit_import[2]) else total_profit_total

            total_cargo_ours = calculate_percentage_mean(cargo_export[0], cargo_import[0]) if '%' in str(cargo_export[0]) or '%' in str(cargo_import[0]) else total_cargo_ours
            total_cargo_agency = calculate_percentage_mean(cargo_export[1], cargo_import[1]) if '%' in str(cargo_export[1]) or '%' in str(cargo_import[1]) else total_cargo_agency
            total_cargo_total = calculate_percentage_mean(cargo_export[2], cargo_import[2]) if '%' in str(cargo_export[2]) or '%' in str(cargo_import[2]) else total_cargo_total
            
            # Add Total data to the table
            html += f"<td style='text-align: center; background-color: #F4CCCC;'>{format_value(total_revenue_ours)}</td>"  # Total Revenue Ours
            html += f"<td style='text-align: center; background-color: #F4CCCC;'>{format_value(total_revenue_agency)}</td>"  # Total Revenue Agency
            html += f"<td style='text-align: center; background-color: #F4CCCC;'>{format_value(total_revenue_total)}</td>"  # Total Revenue Total
            
            html += f"<td style='text-align: center; background-color: #D0E0E3;'>{format_value(total_profit_ours)}</td>"  # Total Profit Ours
            html += f"<td style='text-align: center; background-color: #D0E0E3;'>{format_value(total_profit_agency)}</td>"  # Total Profit Agency
            html += f"<td style='text-align: center; background-color: #D0E0E3;'>{format_value(total_profit_total)}</td>"  # Total Profit Total
            
            html += f"<td style='text-align: center; background-color: #D9EAD3;'>{format_value(total_cargo_ours)}</td>"  # Total Cargo Ours
            html += f"<td style='text-align: center; background-color: #D9EAD3;'>{format_value(total_cargo_agency)}</td>"  # Total Cargo Agency
            html += f"<td style='text-align: center; background-color: #D9EAD3;'>{format_value(total_cargo_total)}</td>"  # Total Cargo Total
            
            html += "</tr>"
        
        # Final replacement for the last period
        if prev_period is not None:
            html = html.replace(f"ROWSPAN_{prev_period}", str(rowspan))
        
        html += "</tbody>"
        html += "</table>"
        return html









    
    # Display the combined HTML table in Streamlit
    if st.session_state["name"] == "Kerem Kuseyri" or st.session_state["name"] == "Üveys Aydemir" or st.session_state["name"] == "Kubilay Cebeci" or st.session_state["name"] == "Senem Çelik" or st.session_state["name"] == "Road Report" or st.session_state["name"] == "Turgut Erkeskin":
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
