import streamlit as st
import joblib
import numpy as np

st.set_page_config(
    page_title="AI Diabetes Prediction",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

/* Main Background */
.stApp{
    background-color:#F5F9FC;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#0F4C81;
}

/* Sidebar text */
[data-testid="stSidebar"] *{
    color:white !important;
}

/* Headings */
h1,h2,h3{
    color:#0F4C81;
}

/* Labels above inputs */
label{
    color:#0F4C81 !important;
    font-weight:bold;
    font-size:16px;
}

/* Number Input - Streamlit 1.58 */

[data-testid="stNumberInput"] input{
    color:#111827 !important;
    -webkit-text-fill-color:#111827 !important;
    opacity:1 !important;
    font-size:16px !important;
    font-weight:600 !important;
    background:transparent !important;
}

[data-testid="stNumberInput"]{
    background:#FFFFFF !important;
    border-radius:10px;
}


/* Buttons */
.stButton>button{
    background:#1976D2;
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    font-size:17px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#0D47A1;
    color:white;
}

/* Metric cards */
[data-testid="stMetric"]{
    background:white;
    padding:15px;
    border-radius:12px;
    border:1px solid #D6EAF8;
    box-shadow:0px 3px 8px rgba(0,0,0,0.08);
}

/* Success box */
.stSuccess{
    border-radius:12px;
}

/* Warning box */
.stWarning{
    border-radius:12px;
}

/* Error box */
.stError{
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.title("🏥 AI Diabetes Predictor")

st.sidebar.success("🤖 Machine Learning Model")

st.sidebar.write("""
**Algorithm**
- Random Forest

**Accuracy**
- 72%

**Dataset**
- 100,000 Patient Records

**Features**
- Age
- BMI
- Blood Pressure
- Cholesterol
- Glucose
- Physical Activity
""")

st.sidebar.divider()

st.sidebar.info(
    "💡 Enter patient details and click **Predict** to estimate diabetes risk."
)

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

st.image("banner.png", use_container_width=True)

st.title("🩺 AI-Based Diabetes Prediction System")
st.success(
    "Helping users estimate diabetes risk through Machine Learning."
)

st.info("🤖 Model Accuracy: 72%")

st.markdown("""
<div style="
padding:15px;
border-radius:15px;
background:#FFFFFF;
box-shadow:0px 2px 10px rgba(0,0,0,0.08);
margin-bottom:20px;">
<h3 style="color:#1565C0;">👤 Enter Patient Details</h3>
</div>
""", unsafe_allow_html=True)
st.caption("Please enter the patient's clinical information below.")


with st.sidebar.expander("📖 About Project"):

    st.markdown("""
### AI-Based Diabetes Prediction System

**Dataset Used**
- Diabetes Health Dataset (100,000 records)

**Algorithm**
- Random Forest Classifier

**Features Used**
- Age
- BMI
- Systolic Blood Pressure
- Diastolic Blood Pressure
- Total Cholesterol
- Fasting Glucose
- Physical Activity

**Target**
- Diagnosed Diabetes (0 = No, 1 = Yes)

**Evaluation Metrics**
- Accuracy : 72%
- Precision : 76.15%
- Recall : 77.21%
- F1-Score : 76.68%
- ROC-AUC : 79.35%
""")
    

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    age = st.number_input(
        "👤 Age (years)",
        min_value=1,
        max_value=120,
        value=30,
        step=1
    )
    st.caption("💡 Enter your age in completed years. Example: 25")

    bmi = st.number_input(
        "⚖️  Body Mass Index (BMI)",
        min_value=10.0,
        max_value=60.0,
        value=25.0,
        step=0.1
    )
    st.caption("💡 BMI measures body weight relative to height. Normal BMI: 18.5 - 24.9")

    sys_bp = st.number_input(
        "❤️ Systolic  Blood Pressure (mmHg)",
        min_value=50,
        max_value=250,
        value=120,
        step=1
    )
    st.caption("💡 Upper blood pressure. Normal range: 90 - 120 mmHg")

with col2:
    dia_bp = st.number_input(
        "💓 Diastolic Blood Pressure (mmHg)",
        min_value=30,
        max_value=150,
        value=80,
        step=1
    )
    st.caption("💡 Lower blood pressure. Normal range: 60 - 80 mmHg")

    chol = st.number_input(
        "🧈 Cholesterol (mg/dL)",
        min_value=50,
        max_value=400,
        value=180,
        step=1
    )
    
    st.caption("💡 Healthy cholesterol level is below 200 mg/dL")

    glucose = st.number_input(
        "🍬 Fasting Glucose (mg/dL)",
        min_value=50,
        max_value=300,
        value=100,
        step=1
    )
    st.caption("💡Blood sugar Before Food.Normal: 70 - 99 mg/dL")

activity = st.number_input(
    "🚶 Physical Activity (minutes/week)",
    min_value=0,
    max_value=300,
    value=150,
    step=5
)
st.caption("💡 Aim for at least 150 minutes of exercise every week.")
col1, col2 = st.columns(2)

with col1:
    predict = st.button(
    "🧠 Predict Diabetes Risk",
    use_container_width=True
)

with col2:
    reset = st.button(
    "🔄 Reset",
    use_container_width=True
)

if reset:
    st.rerun()

if predict:
    try:
        patient = np.array([[
            age,
            bmi,
            sys_bp,
            dia_bp,
            chol,
            glucose,
            activity
        ]], dtype=float)

        

        patient_scaled = scaler.transform(patient)

        
        prediction = model.predict(patient_scaled)[0]

        probability = model.predict_proba(patient_scaled)[0]

        
        risk = probability[1] * 100
        score = 100

        if bmi >= 30:
            score -= 20

        if glucose > 125:
            score -= 25

        if sys_bp >= 140:
            score -= 20

        if activity < 150:
            score -= 15

        st.markdown("---")
        st.subheader("📊 Prediction Dashboard")

        # ---------- First Row ----------
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="📈 Diabetes Risk",
                value=f"{risk:.2f}%"
            )
            st.progress(risk / 100)

        with col2:
            if prediction == 1:
                st.error("🔴 **Prediction: Diabetic**")
            else:
                st.success("🟢 **Prediction: Non-Diabetic**")

        # ---------- Second Row ----------
        col1, col2, col3, col4 = st.columns(4)

        # Risk Level
        with col1:
            if risk >= 70:
                st.metric("Risk Level", "High 🔴")
            elif risk >= 40:
                st.metric("Risk Level", "Moderate 🟡")
            else:
                st.metric("Risk Level", "Low 🟢")

        # BMI
        with col2:
            if bmi < 18.5:
                bmi_status = "Underweight"
            elif bmi < 25:
                bmi_status = "Normal"
            elif bmi < 30:
                bmi_status = "Overweight"
            else:
                bmi_status = "Obese"

            st.metric("BMI", bmi_status)

        # Blood Pressure
        with col3:
            if sys_bp < 120 and dia_bp < 80:
                bp = "Normal"
            elif sys_bp < 130:
                bp = "Elevated"
            elif sys_bp < 140:
                bp = "Stage 1"
            else:
                bp = "Stage 2"

            st.metric("BP", bp)

        # Health Score
        with col4:
            st.metric("Health Score", f"{score}/100")

        st.subheader("📏 BMI Analysis")

        if bmi < 18.5:
            st.warning("Underweight")

        elif bmi < 25:
            st.success("Normal Weight")

        elif bmi < 30:
            st.warning("Overweight")

        else:
            st.error("Obese")

        st.subheader("❤️ Blood Pressure Status")

        if sys_bp < 120 and dia_bp < 80:
            st.success("Normal Blood Pressure")

        elif sys_bp < 130 and dia_bp < 80:
            st.warning("Elevated Blood Pressure")

        elif sys_bp < 140 or dia_bp < 90:
            st.warning("Stage 1 Hypertension")

        else:
            st.error("Stage 2 Hypertension")
        st.subheader("🍬 Glucose Status")

        if glucose < 100:
            st.success("Normal Glucose")

        elif glucose <= 125:
            st.warning("Prediabetes")

        else:
            st.error("Diabetes Range")
        
     

        st.markdown("---")
        st.subheader("📋 Patient Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("👤 Age", f"{age} Years")
            st.metric("❤️ Blood Pressure", f"{sys_bp}/{dia_bp}")

        with col2:
            st.metric("⚖️ BMI", f"{bmi:.1f}")
            st.metric("🧈 Cholesterol", f"{chol} mg/dL")

        with col3:
            st.metric("🍬 Glucose", f"{glucose} mg/dL")
            st.metric("🚶 Activity", f"{activity} min/week")

        st.markdown("---")
        st.subheader("💡 Health Recommendation")

        if risk >= 70:
            st.error("🚨 Consult a healthcare professional immediately.")
            st.success("✔ Reduce sugar intake")
            st.success("✔ Exercise at least 45 minutes daily")
            st.success("✔ Monitor blood glucose regularly")
            st.success("✔ Follow a balanced diabetic diet")

        elif risk >= 40:
            st.warning("⚠ Moderate diabetes risk detected.")
            st.success("✔ Exercise at least 30 minutes daily")
            st.success("✔ Reduce processed sugar")
            st.success("✔ Maintain a healthy weight")
            st.success("✔ Get blood sugar checked regularly")

        else:
            st.success("✔ Continue your healthy lifestyle")
            st.success("✔ Maintain regular physical activity")
            st.success("✔ Eat a balanced diet")
            st.success("✔ Stay hydrated")
            st.success("✔ Schedule routine health checkups")
    except Exception as e:
        st.exception(e)
        st.divider()

st.warning("""
⚠️ **Disclaimer**

This application provides an AI-based diabetes risk prediction for educational purposes only.

It is **not** a substitute for professional medical advice, diagnosis, or treatment.

Always consult a qualified healthcare professional before making medical decisions.
""")
st.divider()

st.caption(
    "🏥 AI-Based Diabetes Prediction System | Developed by Dinesh | B.Tech CSE"
)