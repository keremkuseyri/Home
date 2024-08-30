import pandas as pd
from pymongo import MongoClient
import streamlit as st

st.set_page_config(page_title='Genel Transport', page_icon="https://www.geneltransport.com.tr/wp-content/uploads/2021/03/favicon.png", layout='wide')

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
        budget = f"{month_data.get('budget', 0)}"
        actual = f"{month_data.get('actual', 0)}"
        percentage = f"{month_data.get('percentage', 0)}%"  # Format percentage with "%"
        rows.append([budget, actual, percentage])
    
    # Adding quarterly, half-yearly, and yearly data
    for period in ["quarter_1", "quarter_2", "quarter_3", "quarter_4", 
                   "half_1", "half_2", "year"]:
        period_data = data.get(category, {}).get(period, {})
        budget = f"{period_data.get('budget', 0)}"
        actual = f"{period_data.get('actual', 0)}"
        percentage = f"{period_data.get('percentage', 0)}%"  # Format percentage with "%"
        rows.append([budget, actual, percentage])
    
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
        combined_data.append(r_ours + r_agency + r_total + p_ours + p_agency + p_total + c_ours + c_agency + c_total)

    # Define the multi-index for columns
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
    


# Create DataFrames for Import and Export data
import_combined_df = create_combined_df(import_data[0])
export_combined_df = create_combined_df(export_data[0])




    # Transpose the DataFrame to swap rows and columns
df_transposed_import = import_combined_df.T  

df_transposed_export = export_combined_df.T 
# Display the styled DataFrames in Streamlit
st.write("Import :")
st.dataframe(df_transposed_import, use_container_width=True, height=775)

st.write("Export :")
st.dataframe(df_transposed_export, use_container_width=True, height=775)
