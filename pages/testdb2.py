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
    
    return rows

# Function to structure the data into a single DataFrame
def create_combined_df(data):
    # Extracting the data
    revenue_data = create_category_df(data.get("revenue", {}), "ours") + \
                   create_category_df(data.get("revenue", {}), "agency") + \
                   create_category_df(data.get("revenue", {}), "total")

    profit_data = create_category_df(data.get("profit", {}), "ours") + \
                  create_category_df(data.get("profit", {}), "agency") + \
                  create_category_df(data.get("profit", {}), "total")

    cargo_data = create_category_df(data.get("amount_of_cargo", {}), "ours") + \
                 create_category_df(data.get("amount_of_cargo", {}), "agency") + \
                 create_category_df(data.get("amount_of_cargo", {}), "total")

    # Combining revenue, profit, and cargo data
    combined_data = []
    for r, p, c in zip(revenue_data, profit_data, cargo_data):
        combined_data.append(r + p + c)

    # Create a multi-index for columns as per the Excel format
    column_tuples = [
        ("Revenue", "Ours", "Budget"), ("Revenue", "Ours", "Actual"), ("Revenue", "Ours", "Percentage"),
        ("Revenue", "Agency", "Budget"), ("Revenue", "Agency", "Actual"), ("Revenue", "Agency", "Percentage"),
        ("Revenue", "Total", "Budget"), ("Revenue", "Total", "Actual"), ("Revenue", "Total", "Percentage"),
        ("Profit", "Ours", "Budget"), ("Profit", "Ours", "Actual"), ("Profit", "Ours", "Percentage"),
        ("Profit", "Agency", "Budget"), ("Profit", "Agency", "Actual"), ("Profit", "Agency", "Percentage"),
        ("Profit", "Total", "Budget"), ("Profit", "Total", "Actual"), ("Profit", "Total", "Percentage"),
        ("Cargo", "Ours", "Budget"), ("Cargo", "Ours", "Actual"), ("Cargo", "Ours", "Percentage"),
        ("Cargo", "Agency", "Budget"), ("Cargo", "Agency", "Actual"), ("Cargo", "Agency", "Percentage"),
        ("Cargo", "Total", "Budget"), ("Cargo", "Total", "Actual"), ("Cargo", "Total", "Percentage"),
    ]
    columns = pd.MultiIndex.from_tuples(column_tuples)

    # Define the row labels
    row_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", 
                  "Q1", "Q2", "Q3", "Q4", "H1", "H2", "Year"]

    # Create the DataFrame
    df = pd.DataFrame(combined_data, columns=columns, index=row_labels)
    return df

# Create DataFrames for Import and Export data
import_combined_df = create_combined_df(import_data[0])
export_combined_df = create_combined_df(export_data[0])

# Display in Streamlit
st.write("Import Data Combined:")
st.dataframe(import_combined_df)

st.write("Export Data Combined:")
st.dataframe(export_combined_df)
