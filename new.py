# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="Lifestyle & Health Visualization Dashboard", layout="wide")
st.title("🩺 Lifestyle and Health Condition Dashboard")

# -----------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------
url = "https://raw.githubusercontent.com/ilyajaafar/Assignment/main/dataset.csv"  # Change if needed

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(url)
    except Exception:
        st.warning("⚠️ Could not load from GitHub, please upload manually below.")
        uploaded = st.file_uploader("Upload your dataset (CSV)", type="csv")
        if uploaded:
            df = pd.read_csv(uploaded)
        else:
            st.stop()
    return df

df = load_data()
st.success("✅ Dataset successfully loaded!")
st.write("**Preview of dataset:**")
st.dataframe(df.head())

# -----------------------------------------------------------
# NAVIGATION
# -----------------------------------------------------------
page = st.sidebar.radio(
    "📊 Choose a Dashboard Section:",
    ["Lifestyle & Health Conditions", "Lifestyle by Age & Gender", "Access to Wellness by Region"]
)

# -----------------------------------------------------------
# PAGE 1: Lifestyle & Health Conditions
# -----------------------------------------------------------
if page == "Lifestyle"





