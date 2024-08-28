import streamlit as st
from pymongo import MongoClient

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

# Check if collection is empty
items = list(collection.find({})) + list(collection2.find({}))

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Check if there are any items
if items:
    # Flatten each item and convert to DataFrame
    flattened_items = [flatten_dict(item) for item in items]
    df = pd.DataFrame(flattened_items)
    
    # Display the dataframe in Streamlit
    st.dataframe(df)
else:
    st.write("No items found in the collection.")
