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
# Function to structure the data into a single DataFrame including the Total (Import + Export)
    def create_combined_df(import_data, export_data):
        # Extracting the data for each category
        revenue_ours_import = create_category_df(import_data.get("revenue", {}), "ours")
        revenue_agency_import = create_category_df(import_data.get("revenue", {}), "agency")
        revenue_total_import = create_category_df(import_data.get("revenue", {}), "total")
        
        profit_ours_import = create_category_df(import_data.get("profit", {}), "ours")
        profit_agency_import = create_category_df(import_data.get("profit", {}), "agency")
        profit_total_import = create_category_df(import_data.get("profit", {}), "total")
        
        cargo_ours_import = create_category_df(import_data.get("amount_of_cargo", {}), "ours")
        cargo_agency_import = create_category_df(import_data.get("amount_of_cargo", {}), "agency")
        cargo_total_import = create_category_df(import_data.get("amount_of_cargo", {}), "total")
        
        # Export data
        revenue_ours_export = create_category_df(export_data.get("revenue", {}), "ours")
        revenue_agency_export = create_category_df(export_data.get("revenue", {}), "agency")
        revenue_total_export = create_category_df(export_data.get("revenue", {}), "total")
        
        profit_ours_export = create_category_df(export_data.get("profit", {}), "ours")
        profit_agency_export = create_category_df(export_data.get("profit", {}), "agency")
        profit_total_export = create_category_df(export_data.get("profit", {}), "total")
        
        cargo_ours_export = create_category_df(export_data.get("amount_of_cargo", {}), "ours")
        cargo_agency_export = create_category_df(export_data.get("amount_of_cargo", {}), "agency")
        cargo_total_export = create_category_df(export_data.get("amount_of_cargo", {}), "total")
    
        # Combining the data, including the sum of Import + Export (Total)
        combined_data = []
        for r_ours_imp, r_agency_imp, r_total_imp, p_ours_imp, p_agency_imp, p_total_imp, c_ours_imp, c_agency_imp, c_total_imp, \
            r_ours_exp, r_agency_exp, r_total_exp, p_ours_exp, p_agency_exp, p_total_exp, c_ours_exp, c_agency_exp, c_total_exp in zip(
            revenue_ours_import, revenue_agency_import, revenue_total_import,
            profit_ours_import, profit_agency_import, profit_total_import,
            cargo_ours_import, cargo_agency_import, cargo_total_import,
            revenue_ours_export, revenue_agency_export, revenue_total_export,
            profit_ours_export, profit_agency_export, profit_total_export,
            cargo_ours_export, cargo_agency_export, cargo_total_export
        ):
            # Summing Import and Export values for the Total columns
            total_revenue_ours = r_ours_imp[2] + r_ours_exp[2]
            total_revenue_agency = r_agency_imp[2] + r_agency_exp[2]
            total_revenue_total = r_total_imp[2] + r_total_exp[2]
            
            total_profit_ours = p_ours_imp[2] + p_ours_exp[2]
            total_profit_agency = p_agency_imp[2] + p_agency_exp[2]
            total_profit_total = p_total_imp[2] + p_total_exp[2]
            
            total_cargo_ours = c_ours_imp[2] + c_ours_exp[2]
            total_cargo_agency = c_agency_imp[2] + c_agency_exp[2]
            total_cargo_total = c_total_imp[2] + c_total_exp[2]
            
            combined_data.append([r_ours_imp[2], r_agency_imp[2], r_total_imp[2], 
                                  p_ours_imp[2], p_agency_imp[2], p_total_imp[2], 
                                  c_ours_imp[2], c_agency_imp[2], c_total_imp[2],
                                  r_ours_exp[2], r_agency_exp[2], r_total_exp[2],
                                  p_ours_exp[2], p_agency_exp[2], p_total_exp[2],
                                  c_ours_exp[2], c_agency_exp[2], c_total_exp[2],
                                  total_revenue_ours, total_revenue_agency, total_revenue_total,
                                  total_profit_ours, total_profit_agency, total_profit_total,
                                  total_cargo_ours, total_cargo_agency, total_cargo_total])
    
        # Define the multi-index for columns, adding the new Total category
        column_tuples = [
            ("Revenue", "Ours"), ("Revenue", "Agency"), ("Revenue", "Total"),
            ("Profit", "Ours"), ("Profit", "Agency"), ("Profit", "Total"),
            ("Cargo", "Ours"), ("Cargo", "Agency"), ("Cargo", "Total"),
            ("Revenue", "Ours (Exp)"), ("Revenue", "Agency (Exp)"), ("Revenue", "Total (Exp)"),
            ("Profit", "Ours (Exp)"), ("Profit", "Agency (Exp)"), ("Profit", "Total (Exp)"),
            ("Cargo", "Ours (Exp)"), ("Cargo", "Agency (Exp)"), ("Cargo", "Total (Exp)"),
            ("Total", "Revenue (Ours)"), ("Total", "Revenue (Agency)"), ("Total", "Revenue (Total)"),
            ("Total", "Profit (Ours)"), ("Total", "Profit (Agency)"), ("Total", "Profit (Total)"),
            ("Total", "Cargo (Ours)"), ("Total", "Cargo (Agency)"), ("Total", "Cargo (Total)")
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
    def format_value(value):
        try:
            # Check if the value contains a '%' symbol (indicating a percentage)
            if isinstance(value, str) and '%' in value:
                return value  # Keep as is for percentage strings
            else:
                return f"{int(value):,}".replace(",", ".")  # Replace commas with dots for thousand separator
        except (ValueError, TypeError):
            return value  # Return the value as is if it cannot be converted
    
# Function to create the Total (Import + Export) DataFrame
    def create_total_df(df_import, df_export):
        total_df = df_import.add(df_export, fill_value=0)
        return total_df
    
    # Modify the HTML table creation function to include the Total column
    def create_html_table(df_import, df_export):
        # Calculate Total as Import + Export
        df_total = create_total_df(df_import, df_export)
        
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
        html += "<th colspan='9' style='text-align: center; background-color: #FFD700;'>Total</th>"
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
                        return f"{int(value):,}".replace(",",".")  # Format numbers with commas
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
            
            # Adding Total data (Import + Export)
            revenue_total = df_total.loc[index, ('Revenue', 'Ours')], df_total.loc[index, ('Revenue', 'Agency')], df_total.loc[index, ('Revenue', 'Total')]
            profit_total = df_total.loc[index, ('Profit', 'Ours')], df_total.loc[index, ('Profit', 'Agency')], df_total.loc[index, ('Profit', 'Total')]
            cargo_total = df_total.loc[index, ('Cargo', 'Ours')], df_total.loc[index, ('Cargo', 'Agency')], df_total.loc[index, ('Cargo', 'Total')]
            
            for value in revenue_total:
                html += f"<td style='text-align: center; background-color: #FFD700;'>{format_value(value)}</td>"  # Yellow for Total Revenue
            for value in profit_total:
                html += f"<td style='text-align: center; background-color: #FFD700;'>{format_value(value)}</td>"  # Yellow for Total Profit
            for value in cargo_total:
                html += f"<td style='text-align: center; background-color: #FFD700;'>{format_value(value)}</td>"  # Yellow for Total Cargo
        
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
    if st.session_state["name"] == "Kerem Kuseyri" or st.session_state["name"] == "Üveys Aydemir" or st.session_state["name"] == "Kubilay Cebeci" or st.session_state["name"] == "Senem Çelik" or st.session_state["name"] == "Sea Report" or st.session_state["name"] == "Turgut Erkeskin":
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
