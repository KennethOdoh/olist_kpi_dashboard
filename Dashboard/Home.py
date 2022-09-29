# import required libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title = 'KPI Dashboard',
    page_icon = "📈",
    layout = 'wide',
    
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

# Change data types of listed columns

convert_dtypes = {
        'customer_city': 'category',
        'customer_state': 'category',
        'customer_zip_code_prefix': str,
        'payment_type': 'category',
        'review_score': 'category',
        'seller_city': 'category',
        'seller_state': 'category',
        'order_status' : 'category',
        'product_category_name': 'category'
        }
sales_df = sales_df.astype(convert_dtypes)

# Re-convert columns to desired categorical datatypes
ordered_category ={
    'order_status': ['Unavailable', 'Created', 'Invoiced', 'Approved', 'Processing', 'Shipped', 'Canceled', 'Delivered',],
    'review_score': [1.0, 2.0, 3.0, 4.0, 5.0],
    'payment_type': ['Credit Card', 'Debit Card', 'Voucher', 'Boleto', 'Not Defined',], 
    }

# Convert to categorical datatype
for category in ordered_category:
    ordered_var = pd.api.types.CategoricalDtype(categories=ordered_category[category], ordered = True)
    sales_df[category] = sales_df[category].astype(ordered_var)



# st.dataframe(sales_df)

# filter options
if show_df:
    st.dataframe(sales_df)

st.write(sales_df.info())

def ret_info(df):
    info = df.info()
    return info