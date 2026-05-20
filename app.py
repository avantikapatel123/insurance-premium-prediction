import streamlit as st
import numpy as np
import pickle


model = pickle.load(open("models/model.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))


st.markdown("""
<style>

/* 🌌 Background */
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* 🧊 Main container */
.block-container {
    padding: 2rem;
    border-radius: 20px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
}

/* 🏷️ Title */
h1 {
    text-align: center;
    color: #ffffff;
    font-size: 2.2rem;
    font-weight: bold;
}

/* 🎛️ Inputs */
.stSlider, .stSelectbox {
    border-radius: 10px;
}

/* 🔘 Button */
.stButton>button {
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    color: white !important;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0px 4px 15px rgba(255, 65, 108, 0.4);
}

/* 📦 Success box */
.stAlert {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


st.title("🏥 Insurance Premium Prediction 💰")
st.subheader("Predict your insurance cost instantly ⚡")

age = st.slider("Age", 18, 100)
sex = st.selectbox("Sex", ["male", "female"])
bmi = st.slider("BMI", 10.0, 50.0)
children = st.slider("Children", 0, 5)
smoker = st.selectbox("Smoker", ["yes", "no"])
region = st.selectbox("Region", ["northeast", "northwest", "southeast", "southwest"])


sex = 0 if sex == "male" else 1
smoker = 1 if smoker == "yes" else 0
region = ["northeast", "northwest", "southeast", "southwest"].index(region)

if st.button("Predict 🚀"):
    input_data = np.array([[age, sex, bmi, children, smoker, region]])
    input_data = scaler.transform(input_data)

    prediction = model.predict(input_data)

    st.success(f"💰 Estimated Premium: ₹{prediction[0]:,.2f}")

st.caption("Built with ❤️ using Streamlit + Machine Learning")
