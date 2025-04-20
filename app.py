import streamlit as st
import pickle
import numpy as np
import requests
import os

# Google Drive file ID for the model file
file_id = '1X8ZcS-5WC55i1RXlNxmUwuyoWvJL-9Bs'  # Replace with your actual file ID
model_url = f'https://drive.google.com/uc?id={file_id}'  # Direct file URL for download
model_path = 'linear_regression_model.pkl'

# Function to download the model from Google Drive
def download_model(url, model_path):
    with requests.get(url, stream=True) as r:
        if r.status_code == 200:
            with open(model_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        else:
            st.error("Failed to download the model file")

# Download model if not already downloaded
if not os.path.exists(model_path):
    download_model(model_url, model_path)

# Load the saved model
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Title
st.title("California House Price Prediction")
st.write("Enter the features to predict the house price")

# Pre-filled default values (from the California Housing dataset)
default_values = {
    "MedInc": 5.0,       # Median Income (MedInc)
    "HouseAge": 20.0,    # House Age
    "AveRooms": 5.0,     # Average Rooms
    "AveBedrms": 1.0,    # Average Bedrooms
    "Population": 1000.0, # Population
    "AveOccup": 3.0,     # Average Occupants per Household
    "Latitude": 34.0,    # Latitude
    "Longitude": -118.0  # Longitude
}

# Feature input fields with default values
MedInc = st.number_input("Median Income (MedInc)", min_value=0.0, value=default_values["MedInc"])
HouseAge = st.number_input("House Age", min_value=0.0, value=default_values["HouseAge"])
AveRooms = st.number_input("Average Rooms", min_value=0.0, value=default_values["AveRooms"])
AveBedrms = st.number_input("Average Bedrooms", min_value=0.0, value=default_values["AveBedrms"])
Population = st.number_input("Population", min_value=0.0, value=default_values["Population"])
AveOccup = st.number_input("Average Occupants per Household", min_value=0.0, value=default_values["AveOccup"])
Latitude = st.number_input("Latitude", min_value=0.0, value=default_values["Latitude"])
Longitude = st.number_input("Longitude", min_value=-125.0, value=default_values["Longitude"])

# Prediction
if st.button("Predict House Price"):
    input_data = np.array([[MedInc, HouseAge, AveRooms, AveBedrms,
                            Population, AveOccup, Latitude, Longitude]])
    prediction = model.predict(input_data)[0]
    st.success(f"Predicted Median House Value: ${prediction * 100000:.2f}")
