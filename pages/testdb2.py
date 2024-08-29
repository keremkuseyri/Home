import pandas as pd
from pymongo import MongoClient
import streamlit as st

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
    for month in ["january", "february", "march", "april", "may", "june", 
                  "july", "august", "september", "october", "november", "december"]:
        month_data = data.get(category, {}).get(month, {})
        rows.append([month_data.get("budget", 0), month_data.get("actual", 0), month_data.get("percentage", 0)])
    
    # Adding quarterly, half-yearly, and yearly data
    for period in ["quarter_1", "quarter_2", "quarter_3", "quarter_4", 
                   "half_1", "half_2", "year"]:
        period_data = data.get(category, {}).get(period, {})
        rows.append([period_data.get("budget", 0), period_data.get("actual", 0), period_data.get("percentage", 0)])
    
    # Convert to DataFrame with appropriate row labels
    row_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", 
                  "Q1", "Q2", "Q3", "Q4", "H1", "H2", "Year"]
    df = pd.DataFrame(rows, columns=["Budget", "Actual", "Percentage"], index=row_labels)
    return df

# Function to split data into Revenue, Profit, and Cargo DataFrames
def split_dataframes(data):
    revenue_df_ours = create_category_df(data.get("revenue", {}), "ours")
    revenue_df_agency = create_category_df(data.get("revenue", {}), "agency")
    revenue_df_total = create_category_df(data.get("revenue", {}), "total")
    
    profit_df_ours = create_category_df(data.get("profit", {}), "ours")
    profit_df_agency = create_category_df(data.get("profit", {}), "agency")
    profit_df_total = create_category_df(data.get("profit", {}), "total")
    
    cargo_df_ours = create_category_df(data.get("amount_of_cargo", {}), "ours")
    cargo_df_agency = create_category_df(data.get("amount_of_cargo", {}), "agency")
    cargo_df_total = create_category_df(data.get("amount_of_cargo", {}), "total")
    
    return {
        "Revenue_Ours": revenue_df_ours,
        "Revenue_Agency": revenue_df_agency,
        "Revenue_Total": revenue_df_total,
        "Profit_Ours": profit_df_ours,
        "Profit_Agency": profit_df_agency,
        "Profit_Total": profit_df_total,
        "Cargo_Ours": cargo_df_ours,
        "Cargo_Agency": cargo_df_agency,
        "Cargo_Total": cargo_df_total
    }

# Create DataFrames for Import and Export data
import_dfs = split_dataframes(import_data[0])
export_dfs = split_dataframes(export_data[0])

# Concatenate all import dataframes horizontally
import_combined = pd.concat([
    import_dfs["Revenue_Ours"], import_dfs["Revenue_Agency"], import_dfs["Revenue_Total"],
    import_dfs["Profit_Ours"], import_dfs["Profit_Agency"], import_dfs["Profit_Total"],
    import_dfs["Cargo_Ours"], import_dfs["Cargo_Agency"], import_dfs["Cargo_Total"]
], axis=1)

# Concatenate all export dataframes horizontally
export_combined = pd.concat([
    export_dfs["Revenue_Ours"], export_dfs["Revenue_Agency"], export_dfs["Revenue_Total"],
    export_dfs["Profit_Ours"], export_dfs["Profit_Agency"], export_dfs["Profit_Total"],
    export_dfs["Cargo_Ours"], export_dfs["Cargo_Agency"], export_dfs["Cargo_Total"]
], axis=1)

# Optionally, rename the columns to make them more descriptive
column_names = [
    "Revenue_Ours_Budget", "Revenue_Ours_Actual", "Revenue_Ours_Percentage",
    "Revenue_Agency_Budget", "Revenue_Agency_Actual", "Revenue_Agency_Percentage",
    "Revenue_Total_Budget", "Revenue_Total_Actual", "Revenue_Total_Percentage",
    "Profit_Ours_Budget", "Profit_Ours_Actual", "Profit_Ours_Percentage",
    "Profit_Agency_Budget", "Profit_Agency_Actual", "Profit_Agency_Percentage",
    "Profit_Total_Budget", "Profit_Total_Actual", "Profit_Total_Percentage",
    "Cargo_Ours_Budget", "Cargo_Ours_Actual", "Cargo_Ours_Percentage",
    "Cargo_Agency_Budget", "Cargo_Agency_Actual", "Cargo_Agency_Percentage",
    "Cargo_Total_Budget", "Cargo_Total_Actual", "Cargo_Total_Percentage"
]

import_combined.columns = column_names
export_combined.columns = column_names




st.write("Import Data Combined:")
st.dataframe(import_combined)

st.write("Export Data Combined:")
st.dataframe(export_combined)
