# import required libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title = 'KPI Dashboard',
    page_icon = "📈",
    layout = 'wide'
)


# ---- SIDEBAR ----
st.sidebar.header("Filter Options")
with st.sidebar:
    show_df = st.checkbox(label="Show Data Frame")


st.markdown("###### Olist KPI Dashboard | Home")
st.markdown("---")

# Load Data

@st.cache
def load_data(file_path):
    data = pd.read_csv(file_path, encoding='utf-8')
    return data

sales_df = load_data("../cleaned_sales_data.csv")

# filter options
if show_df:
    st.dataframe(sales_df)

def ret_info(df):
    info = df.info()
    return info

st.write(ret_info(sales_df))

