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



if items:
    for item in items:
        st.write(item)
else:
    st.write("No items found in the collection.")
