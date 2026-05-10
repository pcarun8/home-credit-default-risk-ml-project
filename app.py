import streamlit as st
import pandas as pd
import joblib
from datetime import date


model = joblib.load("best_xgb_model.pkl")

# Exact feature list expected by model
expected_features = [
    'NAME_CONTRACT_TYPE', 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY',
    'CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY',
    'NAME_TYPE_SUITE', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE',
    'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 'REGION_POPULATION_RELATIVE',
    'DAYS_BIRTH', 'DAYS_EMPLOYED', 'DAYS_REGISTRATION', 'DAYS_ID_PUBLISH',
    'FLAG_MOBIL', 'FLAG_WORK_PHONE', 'FLAG_CONT_MOBILE', 'FLAG_PHONE',
    'FLAG_EMAIL', 'OCCUPATION_TYPE', 'CNT_FAM_MEMBERS', 'REGION_RATING_CLIENT',
    'WEEKDAY_APPR_PROCESS_START', 'HOUR_APPR_PROCESS_START',
    'REG_REGION_NOT_LIVE_REGION', 'REG_REGION_NOT_WORK_REGION',
    'LIVE_REGION_NOT_WORK_REGION', 'REG_CITY_NOT_LIVE_CITY',
    'REG_CITY_NOT_WORK_CITY', 'LIVE_CITY_NOT_WORK_CITY', 'ORGANIZATION_TYPE',
    'EXT_SOURCE_2', 'EXT_SOURCE_3', 'OBS_30_CNT_SOCIAL_CIRCLE',
    'DEF_30_CNT_SOCIAL_CIRCLE', 'DEF_60_CNT_SOCIAL_CIRCLE',
    'DAYS_LAST_PHONE_CHANGE', 'FLAG_DOCUMENT_2', 'FLAG_DOCUMENT_3',
    'FLAG_DOCUMENT_4', 'FLAG_DOCUMENT_5', 'FLAG_DOCUMENT_6',
    'FLAG_DOCUMENT_7', 'FLAG_DOCUMENT_8', 'FLAG_DOCUMENT_9',
    'FLAG_DOCUMENT_10', 'FLAG_DOCUMENT_11', 'FLAG_DOCUMENT_12',
    'FLAG_DOCUMENT_13', 'FLAG_DOCUMENT_14', 'FLAG_DOCUMENT_15',
    'FLAG_DOCUMENT_16', 'FLAG_DOCUMENT_17', 'FLAG_DOCUMENT_18',
    'FLAG_DOCUMENT_19', 'FLAG_DOCUMENT_20', 'FLAG_DOCUMENT_21',
    'AMT_REQ_CREDIT_BUREAU_HOUR', 'AMT_REQ_CREDIT_BUREAU_DAY',
    'AMT_REQ_CREDIT_BUREAU_WEEK', 'AMT_REQ_CREDIT_BUREAU_MON',
    'AMT_REQ_CREDIT_BUREAU_QRT', 'AMT_REQ_CREDIT_BUREAU_YEAR'
]


def days_between(past_date, today):
    return -((today - past_date).days)


st.set_page_config(page_title="Home Credit Default Risk Prediction", page_icon="💳")
st.title("🏦 Home Credit Default Risk Prediction")
st.write("Enter applicant details below.")

st.subheader("Applicant Input")

amt_income_total = st.number_input("Total Income", min_value=0.0, value=150000.0, step=1000.0)
amt_credit = st.number_input("Credit Amount", min_value=0.0, value=500000.0, step=1000.0)
amt_annuity = st.number_input("Annuity Amount", min_value=0.0, value=25000.0, step=1000.0)

dob = st.date_input(
    "Date of Birth",
    value=date(1995, 1, 1),
    min_value=date(1940, 1, 1),
    max_value=date.today()
)

employment_start = st.date_input(
    "Employment Start Date",
    value=date(2020, 1, 1),
    min_value=date(1980, 1, 1),
    max_value=date.today()
)


today = date.today()
days_birth = days_between(dob, today)
days_employed = days_between(employment_start, today)

st.write(f"Converted DAYS_BIRTH: {days_birth}")
st.write(f"Converted DAYS_EMPLOYED: {days_employed}")


if st.button("Predict"):
    input_dict = {col: 0 for col in expected_features}

    input_dict['AMT_INCOME_TOTAL'] = amt_income_total
    input_dict['AMT_CREDIT'] = amt_credit
    input_dict['AMT_ANNUITY'] = amt_annuity
    input_dict['DAYS_BIRTH'] = days_birth
    input_dict['DAYS_EMPLOYED'] = days_employed

    input_data = pd.DataFrame([input_dict])[expected_features]

    prediction = model.predict(input_data)[0]

    try:
        probability = model.predict_proba(input_data)[0][1]
    except Exception:
        probability = None

    st.subheader("Prediction Result")

    if prediction == 1:
        st.error("⚠️ High Risk: Client may default")
    else:
        st.success("✅ Low Risk: Client may not default")

    if probability is not None:
        st.write(f"Default Probability: {probability:.2%}")