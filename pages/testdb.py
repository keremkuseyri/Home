import streamlit as st
from pymongo import MongoClient
import pandas as pd

# MongoDB connection string
mongo_uri = "mongodb+srv://kkuseyri:GTTest2024@clusterv0.uwkchdi.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(mongo_uri)

# Use a default database and collection (will be created if they don't exist)
db = client["GTProductImpExp"]
collection = db["Import"]
collection2 = db["Export"]

# Streamlit app
st.write("MongoDB Data Viewer:")

# Fetch all documents from both collections
items_import = list(collection.find({}))
items_export = list(collection2.find({}))

# Function to flatten the nested dictionary structure and arrange it into a table format
def parse_item(item):
    data = {'ours': {}, 'agency': {}, 'total': {}}
    for main_key, main_value in item.items():
        if isinstance(main_value, dict):
            for category, sub_value in main_value.items():  # 'ours', 'agency', 'total'
                if category in data:
                    for period, values in sub_value.items():
                        if period not in data[category]:
                            data[category][period] = {}
                        data[category][period][main_key] = values
    return data

def convert_to_dataframe(parsed_data):
    dfs = {}
    for category in ['ours', 'agency', 'total']:
        data = parsed_data.get(category, {})
        if data:
            df = pd.DataFrame.from_dict(data, orient='index')
            df.index.name = 'Period'
            df.columns = pd.MultiIndex.from_product([[category], df.columns])
            dfs[category] = df
    return dfs

def display_dataframes(dfs, title):
    for category, df in dfs.items():
        st.write(f"{title} - {category.capitalize()}")
        st.dataframe(df)

# Process and display import collection data
if items_import:
    parsed_data_import = [parse_item(item) for item in items_import]
    combined_import_data = {'ours': {}, 'agency': {}, 'total': {}}
    for parsed_data in parsed_data_import:
        for category in combined_import_data:
            combined_import_data[category].update(parsed_data.get(category, {}))
    dfs_import = convert_to_dataframe(combined_import_data)
    display_dataframes(dfs_import, "Import Data")
else:
    st.write("No items found in the Import collection.")

# Process and display export collection data
if items_export:
    parsed_data_export = [parse_item(item) for item in items_export]
    combined_export_data = {'ours': {}, 'agency': {}, 'total': {}}
    for parsed_data in parsed_data_export:
        for category in combined_export_data:
            combined_export_data[category].update(parsed_data.get(category, {}))
    dfs_export = convert_to_dataframe(combined_export_data)
    display_dataframes(dfs_export, "Export Data")
else:
    st.write("No items found in the Export collection.")
