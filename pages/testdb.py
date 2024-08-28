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
    data = {}
    for main_key, main_value in item.items():
        if isinstance(main_value, dict):
            for sub_key, sub_value in main_value.items():
                if isinstance(sub_value, dict):
                    for metric, values in sub_value.items():
                        if metric not in data:
                            data[metric] = {}
                        for period, value in values.items():
                            if period not in data[metric]:
                                data[metric][period] = {}
                            data[metric][period][sub_key] = value
    return data

def convert_to_dataframe(parsed_data):
    dfs = []
    for metric, periods in parsed_data.items():
        df = pd.DataFrame.from_dict(periods, orient='index')
        df.index.name = 'Period'
        df.columns = pd.MultiIndex.from_product([[metric], df.columns])
        dfs.append(df)
    return pd.concat(dfs, axis=1)

# Check if there are any items in import collection
if items_import:
    parsed_data_import = [parse_item(item) for item in items_import]
    combined_import_data = {k: v for d in parsed_data_import for k, v in d.items()}
    df_import = convert_to_dataframe(combined_import_data)
    st.write("Import Data")
    st.dataframe(df_import)
else:
    st.write("No items found in the Import collection.")

# Check if there are any items in export collection
if items_export:
    parsed_data_export = [parse_item(item) for item in items_export]
    combined_export_data = {k: v for d in parsed_data_export for k, v in d.items()}
    df_export = convert_to_dataframe(combined_export_data)
    st.write("Export Data")
    st.dataframe(df_export)
else:
    st.write("No items found in the Export collection.")
