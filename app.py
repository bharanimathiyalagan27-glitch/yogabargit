import streamlit as st
import pandas as pd

st.set_page_config(page_title="Yogarbar Dashboard", layout="wide")

st.title("📊 Yogarbar Sales Dashboard")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    return pd.read_excel("data.xlsx")

df = load_data()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("🔍 Filters")

if "Product" in df.columns:
    product_filter = st.sidebar.multiselect(
        "Select Product",
        options=df["Product"].unique(),
        default=df["Product"].unique()
    )
    df = df[df["Product"].isin(product_filter)]

if "Region" in df.columns:
    region_filter = st.sidebar.multiselect(
        "Select Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )
    df = df[df["Region"].isin(region_filter)]

# ---------- KPI ----------
st.subheader("📌 Key Metrics")

col1, col2 = st.columns(2)

if "Sales" in df.columns:
    col1.metric("Total Sales", f"₹{df['Sales'].sum():,.0f}")

col2.metric("Total Records", len(df))

# ---------- CHART ----------
st.subheader("📈 Sales Chart")

numeric_cols = df.select_dtypes(include="number").columns

if len(numeric_cols) > 0:
    selected_col = st.selectbox("Select metric", numeric_cols)
    st.bar_chart(df[selected_col])

# ---------- DATA ----------
with st.expander("🔎 View Data"):
    st.dataframe(df)

# ---------- SIMPLE CHATBOT (rule based for now) ----------
st.subheader("🤖 Data Chatbot")

question = st.text_input("Ask about sales")

if question:
    if "total sales" in question.lower():
        st.write(f"Total sales is ₹{df['Sales'].sum():,.0f}")
    elif "total records" in question.lower():
        st.write(f"Total records are {len(df)}")
    else:
        st.write("I can answer basic questions like total sales.")
