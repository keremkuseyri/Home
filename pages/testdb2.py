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
    for month in ["January", "February", "March", "April", "May", "June", 
                  "July", "August", "September", "October", "November", "December"]:
        month_data = data.get(category, {}).get(month.lower(), {})
        budget = month_data.get("budget", 0)
        actual = month_data.get("actual", 0)
        percentage = month_data.get("percentage", "0%")
        rows.extend([(month, 'Budget', budget), (month, 'Actual', actual), (month, '+/- %', percentage)])
    
    # Adding quarterly, half-yearly, and yearly data
    for period in [("Q1", "quarter_1"), ("Q2", "quarter_2"), ("Q3", "quarter_3"), ("Q4", "quarter_4"), 
                   ("H1", "half_1"), ("H2", "half_2"), ("Year", "year")]:
        period_data = data.get(category, {}).get(period[1], {})
        budget = period_data.get("budget", 0)
        actual = period_data.get("actual", 0)
        percentage = period_data.get("percentage", "0%")
        rows.extend([(period[0], 'Budget', budget), (period[0], 'Actual', actual), (period[0], '+/- %', percentage)])
    
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

    # Convert percentage strings to numbers where possible
    for i in range(len(combined_data)):
        for j in range(len(combined_data[i])):
            if isinstance(combined_data[i][j], str) and combined_data[i][j].endswith('%'):
                combined_data[i][j] = combined_data[i][j][:-1]  # Remove % symbol
            try:
                combined_data[i][j] = float(combined_data[i][j])  # Convert to float
            except ValueError:
                continue  # If conversion fails, keep the original value

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
    
    # Adding 2024 header
    df.columns = pd.MultiIndex.from_product([["2024"], columns])

    return df

# Create DataFrames for Import and Export data
import_combined_df = create_combined_df(import_data[0])
export_combined_df = create_combined_df(export_data[0])

# Function to apply styling to DataFrame
def style_dataframe(df, title):
    def highlight_columns(col):
        if col.name[1][0] == "Revenue":
            return ['background-color: #00B0F0'] * len(col)
        elif col.name[1][0] == "Profit":
            return ['background-color: #92D050'] * len(col)
        elif col.name[1][0] == "Cargo":
            return ['background-color: #00B050'] * len(col)
        return [''] * len(col)

    # Apply the styling
    styled_df = df.style.apply(highlight_columns, axis=1)
    
    # Add a title that spans all columns
    styled_df.set_caption(f"<h1 style='text-align: center; color: black'>{title}</h1>")
    
    return styled_df

# Apply styling to the DataFrames
import_styled_df = style_dataframe(import_combined_df, "Import 2024")  
export_styled_df = style_dataframe(export_combined_df, "Export 2024")  

# Display the styled DataFrames in Streamlit
st.write("Import:")
st.dataframe(import_styled_df, use_container_width=True, height=775)

st.write("Export:")
st.dataframe(export_styled_df, use_container_width=True, height=775)
