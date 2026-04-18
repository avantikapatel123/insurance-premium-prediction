import streamlit as st
import numpy as np
import pickle

# model load
model = pickle.load(open("models/model.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

st.markdown("""
<style>


body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.main {
    background: rgba(255, 255, 255, 0.05);
    padding: 30px;
    border-radius: 20px;
}


.block-container {
    padding: 2rem;
    border-radius: 20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
}


button {
    background-color: #ff4b2b !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    border: none !important;
    cursor: pointer !important;
}

button:hover {
    background-color: #ff416c !important;
}


.stSlider, .stSelectbox {
    border-radius: 10px;
}


h1 {
    text-align: center;
    color: #ffffff;
}

</style>
""", unsafe_allow_html=True)

st.title("Insurance Premium Prediction 💰")

# inputs
age = st.slider("Age", 18, 100)
sex = st.selectbox("Sex", ["male", "female"])
bmi = st.slider("BMI", 10.0, 50.0)
children = st.slider("Children", 0, 5)
smoker = st.selectbox("Smoker", ["yes", "no"])
region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"])

# convert
sex = 0 if sex == "male" else 1
smoker = 1 if smoker == "yes" else 0
region = ["northeast", "northwest", "southeast", "southwest"].index(region)

# predict
if st.button("Predict"):
    input_data = np.array([[age, sex, bmi, children, smoker, region]])
    input_data = scaler.transform(input_data)

    prediction = model.predict(input_data)

    st.success(f"Estimated Premium: ₹{prediction[0]:,.2f}")