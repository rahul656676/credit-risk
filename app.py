import streamlit as st
import pandas as pd
import joblib

# =========================
# LOAD MODEL
# =========================

model = joblib.load("credit_model.pkl")

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Credit Risk Management System",
    page_icon="🏦",
    layout="centered"
)

# =========================
# TITLE
# =========================

st.title("🏦 Credit Risk Management System")

st.write("Predict whether a customer is eligible for loan approval.")

# =========================
# USER INPUTS
# =========================

age = st.slider(
    "Age",
    18,
    70
)

gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

monthly_income = st.number_input(
    "Monthly Income (₹)",
    min_value=1000,
    step=1000
)

loan_amount = st.number_input(
    "Loan Amount (₹)",
    min_value=1000,
    step=5000
)

duration = st.slider(
    "Loan Duration (Months)",
    1,
    60
)

interest_rate = st.slider(
    "Interest Rate (%)",
    1.0,
    25.0
)

job = st.selectbox(
    "Job Type",
    ["Unskilled", "Skilled", "Highly Skilled"]
)

# =========================
# ENCODING
# =========================

gender_value = 1 if gender == "Male" else 0

job_map = {
    "Unskilled": 0,
    "Skilled": 1,
    "Highly Skilled": 2
}

job_value = job_map[job]

# =========================
# BUTTON
# =========================

if st.button("Predict Loan Risk"):

    # =========================
    # EMI CALCULATION
    # =========================

    monthly_interest = interest_rate / 12 / 100

    emi = (
        loan_amount *
        monthly_interest *
        (1 + monthly_interest) ** duration
    ) / (
        ((1 + monthly_interest) ** duration) - 1
    )

    total_payment = emi * duration
    total_interest = total_payment - loan_amount

    # =========================
    # MODEL INPUT
    # =========================

    input_data = pd.DataFrame({
        'Unnamed: 0': [0],
        'Age': [age],
        'Sex': [gender_value],
        'Job': [job_value],
        'Housing': [1],
        'Saving accounts': [1],
        'Checking account': [1],
        'Credit amount': [loan_amount],
        'Duration': [duration],
        'Purpose': [1]
    })

    # =========================
    # ML PREDICTION
    # =========================

    prediction = model.predict(input_data)

    # =========================
    # CUSTOM RISK LOGIC
    # =========================

    risk_score = 0

    # Loan vs Income Ratio

    if loan_amount > monthly_income * 50:
        risk_score += 5

    elif loan_amount > monthly_income * 20:
        risk_score += 3

    elif loan_amount > monthly_income * 10:
        risk_score += 2

    # High Interest Rate

    if interest_rate > 15:
        risk_score += 2

    # Very Long Duration

    if duration > 48:
        risk_score += 1

    # Unskilled Job

    if job == "Unskilled":
        risk_score += 2

    # Very Young Applicant

    if age < 21:
        risk_score += 1

    # =========================
    # EMI AFFORDABILITY
    # =========================

    # EMI greater than 75% salary

    if emi > monthly_income * 0.75:
        risk_score += 5

    # EMI between 60% and 75%

    elif emi > monthly_income * 0.60:
        risk_score += 2

    # =========================
    # FINAL RESULT
    # =========================

    st.subheader("Prediction Result")

    if prediction[0] == 1 or risk_score >= 5:

        st.error(
            "❌ High Credit Risk — Loan Not Recommended"
        )

    else:

        st.success(
            "✅ Low Credit Risk — Loan Can Be Approved"
        )

    # =========================
    # LOAN DETAILS
    # =========================

    st.subheader("Loan Details")

    st.info(f"💰 Monthly EMI: ₹{emi:.2f}")

    st.info(f"📈 Total Interest: ₹{total_interest:.2f}")

    st.info(f"🏦 Total Payment: ₹{total_payment:.2f}")

    # =========================
    # EMI ANALYSIS
    # =========================

    st.subheader("EMI Analysis")

    salary_ratio = (emi / monthly_income) * 100

    st.write(
        f"EMI consumes {salary_ratio:.2f}% of monthly income"
    )

    if salary_ratio > 75:

        st.error(
            "⚠️ EMI is too high compared to income"
        )

    elif salary_ratio > 60:

        st.warning(
            "⚠️ EMI is moderately high"
        )

    else:

        st.success(
            "✅ EMI is financially manageable"
        )

    # =========================
    # RISK ANALYSIS
    # =========================

    st.subheader("Risk Analysis")

    st.write(f"Risk Score: {risk_score}")

    if risk_score >= 5:

        st.warning(
            "Customer profile shows high repayment risk."
        )

    else:

        st.success(
            "Customer profile looks financially stable."
        )