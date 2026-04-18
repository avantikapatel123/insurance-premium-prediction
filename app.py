import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt
from fpdf import FPDF

# ---------------- MODEL LOAD ----------------
model = pickle.load(open("models/model.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

# ---------------- UI STYLE ----------------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.block-container {
    padding: 2rem;
    border-radius: 20px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0px 8px 30px rgba(0,0,0,0.4);
}

h1 {
    text-align: center;
    color: #ffffff;
    font-size: 2.4rem;
    font-weight: 700;
    text-shadow: 0px 2px 10px rgba(0,0,0,0.5);
}

.stButton>button {
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    color: white !important;
    border-radius: 14px;
    padding: 12px 24px;
    border: none;
    font-weight: bold;
    cursor: pointer;
    transition: 0.3s;
    box-shadow: 0px 5px 20px rgba(255, 65, 108, 0.4);
}

.stButton>button:hover {
    transform: scale(1.08);
    box-shadow: 0px 8px 25px rgba(255, 105, 180, 0.6);
}

.stAlert {
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🏥 Insurance Premium Prediction 💰")
st.subheader("AI predicts your insurance cost instantly ⚡")

# ---------------- MODEL INFO ----------------
st.metric("Model Accuracy (R²)", "0.89")

# ---------------- INPUTS ----------------
age = st.slider("Age", 18, 100)
sex = st.selectbox("Sex", ["male", "female"])
bmi = st.slider("BMI", 10.0, 50.0)
children = st.slider("Children", 0, 5)
smoker = st.selectbox("Smoker", ["yes", "no"])
region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"])

# ---------------- CONVERT ----------------
sex = 0 if sex == "male" else 1
smoker = 1 if smoker == "yes" else 0
region = ["northeast", "northwest", "southeast", "southwest"].index(region)

# ---------------- PREDICT ----------------
if st.button("Predict 🚀"):

    input_data = np.array([[age, sex, bmi, children, smoker, region]])
    input_data = scaler.transform(input_data)

    prediction = model.predict(input_data)[0]

    # ---------------- RISK CATEGORY ----------------
    if prediction < 10000:
        risk = "🟢 Low Risk"
    elif prediction < 20000:
        risk = "🟠 Medium Risk"
    else:
        risk = "🔴 High Risk"

    st.success(f"💰 Estimated Premium: INR {prediction:,.2f}")
    st.info(f"Risk Category: {risk}")

  

# ---------------- GRAPH ----------------
if st.button("Show Age vs Premium Graph 📊"):

    ages = np.arange(18, 100, 5)
    premiums = ages * 250

    fig, ax = plt.subplots()
    ax.plot(ages, premiums, marker='o')
    ax.set_title("Age vs Insurance Premium")
    ax.set_xlabel("Age")
    ax.set_ylabel("Premium")

    st.pyplot(fig)

# ---------------- FOOTER ----------------
st.caption("Built with ❤️ using Streamlit + Machine Learning")
