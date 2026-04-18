import streamlit as st
import numpy as np
import pickle

# ---------------- MODEL LOAD ----------------
model = pickle.load(open("models/model.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

# ---------------- UI STYLE (BLACK + BROWN DARK THEME) ----------------
st.markdown("""
<style>

/* 🌑 Dark Black Background */
body {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a0d07 50%, #2d1b11 100%);
}

/* 🖥️ Main container (WIDER + TALLER) */
.block-container {
    padding: 2rem 2.5rem !important;
    max-width: 950px !important;
    margin: auto;
    min-height: 80vh;
    border-radius: 25px;
    background: rgba(20, 20, 20, 0.95);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(139, 69, 19, 0.4);
    box-shadow: 
        0px 15px 40px rgba(0,0,0,0.8),
        inset 0px 1px 0px rgba(255,255,255,0.1);
}

/* 🏷️ Title (Bigger & Bold) */
h1 {
    text-align: center;
    color: #d4af37;
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 1rem;
    text-shadow: 
        0px 0px 20px rgba(212, 175, 55, 0.5),
        0px 2px 10px rgba(0,0,0,0.8);
    letter-spacing: 2px;
}

/* 🔤 Subheader */
h2 {
    color: #b8860b;
    font-weight: 600;
    text-shadow: 0px 2px 8px rgba(0,0,0,0.7);
}

/* 🎛️ Input Containers (Wider) */
.stSlider, .stSelectbox {
    border-radius: 15px !important;
    padding: 0.8rem !important;
}

/* 📦 Input Boxes */
div[data-baseweb="input"] {
    box-shadow: 
        0px 8px 25px rgba(0,0,0,0.6),
        inset 0px 1px 0px rgba(255,255,255,0.05);
    border-radius: 12px;
    border: 1px solid rgba(184, 134, 11, 0.3);
    background: rgba(30, 30, 30, 0.9);
}

/* 🔘 BUTTON (Black + Gold Brown) */
.stButton>button {
    background: linear-gradient(145deg, #1a1a1a 0%, #2d1b11 50%, #4a2c0f 100%);
    color: #ffd700 !important;
    border-radius: 18px;
    padding: 14px 30px;
    border: 2px solid rgba(255, 215, 0, 0.3);
    font-weight: 700;
    font-size: 1.1rem;
    cursor: pointer !important;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    box-shadow: 
        0px 8px 25px rgba(45, 27, 17, 0.7),
        inset 0px 1px 0px rgba(255,255,255,0.1);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* 🔥 BUTTON HOVER (Fire Effect) */
.stButton>button:hover {
    transform: translateY(-3px) scale(1.03);
    background: linear-gradient(145deg, #3a2a15 0%, #5a3a20 50%, #8b4513 100%);
    color: #fff !important;
    box-shadow: 
        0px 15px 35px rgba(139, 69, 19, 0.8),
        0px 0px 30px rgba(255, 215, 0, 0.4);
    border-color: rgba(255, 215, 0, 0.6);
}

/* 📊 Output Boxes */
.stSuccess, .stInfo {
    border-radius: 18px;
    box-shadow: 
        0px 10px 30px rgba(0,0,0,0.7),
        inset 0px 1px 0px rgba(255,255,255,0.05);
    border-left: 5px solid #ffd700;
    background: rgba(45, 27, 17, 0.9);
    backdrop-filter: blur(10px);
}

/* ✨ Labels (Gold Brown) */
label {
    color: #ffd700 !important;
    font-weight: 600;
    font-size: 1rem;
    text-shadow: 0px 1px 3px rgba(0,0,0,0.8);
}

/* 🖱️ Enhanced Cursor */
button, select, input {
    cursor: pointer !important;
}

/* 📱 Responsive */
@media (max-width: 768px) {
    .block-container {
        padding: 1.5rem 1.5rem !important;
        max-width: 95% !important;
    }
    h1 {
        font-size: 2.2rem;
    }
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🏥 Insurance Premium Predictor 💰")
st.subheader("Get instant premium prediction ⚡")

# ---------------- INPUTS (Better Spacing) ----------------
col1, col2 = st.columns(2)

with col1:
    age = st.slider("👤 Age", 18, 100, 30)
    sex = st.selectbox("⚥ Sex", ["male", "female"])
    
with col2:
    bmi = st.slider("📏 BMI", 10.0, 50.0, 25.0)
    children = st.slider("👨‍👩‍👧‍👦 Children", 0, 5, 1)

smoker = st.selectbox("🚬 Smoker", ["yes", "no"])
region = st.selectbox("📍 Region", ["northeast", "northwest", "southeast", "southwest"])

# ---------------- CONVERT ----------------
sex = 0 if sex == "male" else 1
smoker = 1 if smoker == "yes" else 0
region = ["northeast", "northwest", "southeast", "southwest"].index(region)

# ---------------- PREDICT ----------------
if st.button("🔮 Predict Premium 🚀", use_container_width=True):
    input_data = np.array([[age, sex, bmi, children, smoker, region]])
    input_data = scaler.transform(input_data)

    prediction = model.predict(input_data)
    premium = prediction[0]

    # 🔥 Risk Category Logic
    if premium < 10000:
        risk = "🟢 LOW RISK"
        risk_color = "🟢"
    elif premium < 30000:
        risk = "🟡 MEDIUM RISK"
        risk_color = "🟡"
    else:
        risk = "🔴 HIGH RISK"
        risk_color = "🔴"

    st.success(f"💰 **Estimated Premium:** ₹{premium:,.2f}")
    st.info(f"📊 **Risk Category:** {risk_color} {risk}")

# footer
st.markdown("---")
st.caption("🔥 Built with ❤️ using Streamlit + Machine Learning")
