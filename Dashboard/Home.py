# import required libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# Page configurations
st.set_page_config(
    page_title = 'KPI Dashboard',
    page_icon = "📈",
    layout = 'wide',
    
)

# Load Data
@st.cache
def load_data(file_path, encoding='utf-8'):
    '''Fetch data from source file, and apply pandas-specific data type transformation.
    return: the transformed dataframe'''
    df = pd.read_csv(file_path, encoding=encoding)

    # Change data types of listed columns
    convert_dtypes = {
            'order_purchase_timestamp': 'datetime64',
            'order_approved_at': 'datetime64',
            'order_delivered_customer_date': 'datetime64',
            'customer_city': 'category',
            'customer_state': 'category',
            'customer_zip_code_prefix': 'str',
            'payment_type': 'category',
            'review_score': 'category',
            'seller_zip_code_prefix': 'str',
            'seller_city': 'category',
            'seller_state': 'category',
            'order_status' : 'category',
            'product_category_name_english': 'category'
            }
    df = df.astype(convert_dtypes)

    # Re-convert columns to desired categorical datatypes
    ordered_category ={
        'order_status': ['Unavailable', 'Created', 'Invoiced', 'Approved', 'Processing', 'Shipped', 'Canceled', 'Delivered',],
        'review_score': [1.0, 2.0, 3.0, 4.0, 5.0],
        'payment_type': ['Credit Card', 'Debit Card', 'Voucher', 'Boleto', 'Not Defined',], 
        }

    # Convert to categorical datatype
    for category in ordered_category:
        ordered_var = pd.api.types.CategoricalDtype(categories=ordered_category[category], ordered = True)
        df[category] = df[category].astype(ordered_var)

    return df

sales_df = load_data("../cleaned_sales_data.csv")


# ---- SIDEBAR ----
st.sidebar.header("Filter Options")
with st.sidebar:
    show_df = st.checkbox(label="Show Data Frame", value=True)

# FIRST HORIZONTAL BAR AT THE HOME PAGE
st.markdown("###### Olist KPI Dashboard | Home")
st.markdown("---")


# FIRST ROW: 3 COLUMN CARD LAYOUT
st.subheader('Sales')
col11, col21, col31, col41 = st.columns(4, gap='medium')

with col11:
    st.metric(label='Target', value = "$2M", delta= -12, help = 'Target for this year compared to that of last year')
with col21:
    st.metric(label='Target', value = "$2M", delta= -12, help = 'Target for this year compared to that of last year')
with col31:
    st.metric(label='Target', value = "$2M", delta= -12, help = 'Target for this year compared to that of last year')
with col41:
    st.metric(label='Target', value = "$2M", delta= -12, help = 'Target for this year compared to that of last year')


# SECOND HORIZONTAL BAR AT THE HOME PAGE
st.markdown("---")
# filter options
sales_by_product_category = (
    sales_df.groupby(by=['product_category_name_english']).sum()['payment_value'].sort_values()
)
fig_product_sales = px.bar(
    sales_by_product_category,
)
if show_df:
    st.dataframe(sales_df)

