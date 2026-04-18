import streamlit as st
import numpy as np
import pickle
import os

st.title("Insurance Premium Prediction 💰")

# safe path handling
model_path = os.path.join("models", "model.pkl")
scaler_path = os.path.join("models", "scaler.pkl")

try:
    model = pickle.load(open(model_path, "rb"))
    scaler = pickle.load(open(scaler_path, "rb"))
    model_loaded = True
except Exception as e:
    st.error(f"Model load error: {e}")
    model_loaded = False

# inputs
age = st.slider("Age", 18, 100)
sex = st.selectbox("Sex", ["male", "female"])
bmi = st.slider("BMI", 10.0, 50.0)
children = st.slider("Children", 0, 5)
smoker = st.selectbox("Smoker", ["yes", "no"])
region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"])

sex = 0 if sex == "male" else 1
smoker = 1 if smoker == "yes" else 0
region = ["northeast", "northwest", "southeast", "southwest"].index(region)

if st.button("Predict"):
    if model_loaded:
        input_data = np.array([[age, sex, bmi, children, smoker, region]])
        input_data = scaler.transform(input_data)
        prediction = model.predict(input_data)
        st.success(f"Estimated Premium: ₹{prediction[0]:,.2f}")
    else:
        st.warning("Model not loaded properly ❌ Check logs")
