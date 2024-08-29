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
        budget = month_data.get("budget", 0)
        actual = month_data.get("actual", 0)
        percentage = f"{month_data.get('percentage', 0)}%"
        rows.append([budget, actual, percentage])
    
    # Adding quarterly, half-yearly, and yearly data
    for period in ["quarter_1", "quarter_2", "quarter_3", "quarter_4", 
                   "half_1", "half_2", "year"]:
        period_data = data.get(category, {}).get(period, {})
        budget = period_data.get("budget", 0)
        actual = period_data.get("actual", 0)
        percentage = f"{period_data.get('percentage', 0)}%"
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
        ("Revenue", "Ours"), ("Revenue", "Agency"), ("Revenue", "Total"),
        ("Profit", "Ours"), ("Profit", "Agency"), ("Profit", "Total"),
        ("Cargo", "Ours"), ("Cargo", "Agency"), ("Cargo", "Total"),
    ]
    columns = pd.MultiIndex.from_tuples(column_tuples)

    # Define the row labels
    row_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", 
                  "Q1", "Q2", "Q3", "Q4", "H1", "H2", "Year"]

    # Create the DataFrame
    df = pd.DataFrame(combined_data, columns=columns, index=row_labels)

    # Concatenate Budget, Actual, and Percentage columns
    def format_column(col):
        if col.name[0] in ["Revenue", "Profit", "Cargo"]:
            category = col.name[0]
            return df[category].apply(lambda x: f"{x[0]}, {x[1]}, {x[2]}")
        return df[col.name]

    formatted_df = df.apply(format_column, axis=0)
    formatted_df.columns = pd.MultiIndex.from_product([["Revenue", "Profit", "Cargo"], ["Ours", "Agency", "Total"]])

    return formatted_df

# Create DataFrames for Import and Export data
import_combined_df = create_combined_df(import_data[0])
export_combined_df = create_combined_df(export_data[0])

# Function to apply styling to DataFrame
def style_dataframe(df):
    def highlight_columns(col):
        if col.name[0] == "Revenue":
            return ['background-color: #00B0F0'] * len(col)
        elif col.name[0] == "Profit":
            return ['background-color: #92D050'] * len(col)
        elif col.name[0] == "Cargo":
            return ['background-color: #00B050'] * len(col)
        return [''] * len(col)

    def highlight_index(row):
        return ['background-color: #FFC000'] * len(row)

    # Apply the styling
    styled_df = df.style.apply(highlight_columns, axis=0)
    
    # Set other style options (optional)
    styled_df.set_properties(**{'text-align': 'center'})
    
    return styled_df

# Apply styling to the DataFrames
import_styled_df = style_dataframe(import_combined_df)
export_styled_df = style_dataframe(export_combined_df)

# Display the styled DataFrames in Streamlit
st.write("Import Data Combined:")
st.dataframe(import_styled_df, use_container_width=True)

st.write("Export Data Combined:")
st.dataframe(export_styled_df, use_container_width=True)
