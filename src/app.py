import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression

st.title("The Crop Management System")

# Crop Prediction Section
st.header("Crop Prediction")
temp = st.number_input("Enter Temperature (°C)")
humidity = st.number_input("Enter Humidity (%)")
soil_type = st.selectbox("Select Soil Type", ["Sandy", "Loamy", "Clay"])
rainfall = st.number_input("Enter Rainfall (mm)")

# Soil Type Encoding
soil_type_map = {"Sandy": 0, "Loamy": 1, "Clay": 2}
soil_type_encoded = soil_type_map[soil_type]

if st.button("Predict Crop"):
    # Sample trained model for demonstration
    model = RandomForestClassifier()
    # Placeholder dataset for example
    model.fit([[22, 80, 0, 200], [24, 82, 1, 250]], ["Rice", "Wheat"])
    prediction = model.predict([[temp, humidity, soil_type_encoded, rainfall]])
    st.success(f"Recommended Crop: {prediction[0]}")

# Fertilizer Recommendation Section
st.header("Fertilizer Recommendation")

if st.button("Recommend Fertilizer"):
    # Simple fertilizer recommendation based on soil type
    if soil_type == "Sandy":
        fertilizer = "Use nitrogen-rich fertilizers like Urea."
    elif soil_type == "Loamy":
        fertilizer = "Use balanced fertilizers like NPK."
    else:
        fertilizer = "Use phosphate fertilizers like Superphosphate."

    st.success(f"Recommended Fertilizer: {fertilizer}")

# Yield Prediction Section
st.header("Rainfall and Yield Prediction")
rainfall_input = st.number_input("Enter Rainfall for Yield Prediction (mm)")
year_input = st.number_input("Enter Year")

if st.button("Predict Yield"):
    # Placeholder linear regression model
    yield_model = LinearRegression()
    # Placeholder dataset for example
    yield_model.fit([[2015, 200], [2016, 220]], [2.5, 2.7])
    yield_prediction = yield_model.predict([[year_input, rainfall_input]])
    st.success(f"Predicted Yield: {yield_prediction[0]:.2f} tons")
