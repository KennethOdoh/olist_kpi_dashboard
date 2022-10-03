# import required libraries
from tkinter.ttk import Style
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from millify import millify

# Page configurations
st.set_page_config(
    page_title = 'KPI Dashboard',
    page_icon = "📈",
    layout = 'wide',
    
)
hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

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
st.markdown("#### 📈 Sales Dashboard `Home`")
st.markdown("---")

this_year = sales_df.year.max()
last_year = this_year - 1

def total_cleared_order():
    '''Value of orders already delivered to customers THIS year'''
    total_cleared_order = sales_df.query("order_status == 'Delivered'").query("year == @this_year")['payment_value'].sum()
    return int(total_cleared_order)

def total_cleared_order_last_year():
    '''Value of orders delivered to customers LAST year'''
    total_cleared_order_last_year = sales_df.query("order_status == 'Delivered'").query("year == @last_year")['payment_value'].sum()
    return int(total_cleared_order_last_year)

def total_canceled_order():
    '''Value of orders that were canceled THIS year'''
    total_canceled_order = sales_df.query("order_status == 'Canceled'").query("year == @this_year")['payment_value'].sum()
    return int(total_canceled_order)

def total_canceled_order_last_year():
    '''Value of orders that were canceled LAST year'''
    total_canceled_order_last_year = sales_df.query("order_status == 'Canceled'").query("year == @last_year")['payment_value'].sum()
    return int(total_canceled_order_last_year)

# YoY Growth
# formula = (revenue this year - revenue last year)/revenue last year * 100
def YoY_growth(this_year, last_year):
    revenue_this_year = sales_df.query("year == @this_year").payment_value.sum()
    revenue_last_year = sales_df.query("year == @last_year").payment_value.sum()    
    difference = revenue_this_year - revenue_last_year
    yoy_growth = (difference / revenue_last_year) * 100
    return int(yoy_growth)



# FIRST ROW: 3 COLUMN CARD LAYOUT
st.subheader('KPIs')
col11, col21, col31, col41 = st.columns(4, gap='medium')

with col11:
    total_cleared_order = total_cleared_order()
    total_cleared_order_last_year = total_cleared_order_last_year()
    st.metric(label='CLEARED ORDERS', value = "${}".format(millify(total_cleared_order, precision= 2)), 
    delta = millify(total_cleared_order - total_cleared_order_last_year),
    help = 'Value of orders already delivered to customers this year, compared to last year')

with col21:
    total_canceled_order = total_canceled_order()
    total_canceled_order_last_year = total_canceled_order_last_year()
    st.metric(label='CANCELLED ORDERS', value = "${}".format(millify(total_canceled_order, precision= 2)), 
    delta= millify(total_canceled_order - total_canceled_order_last_year),
    help = 'Value of orders that were canceled this year, compared to last year',
    delta_color="inverse",
    )

with col31:
    yoy_growth = YoY_growth(this_year, last_year)
    yoy_growth_last_year = YoY_growth(last_year, last_year-1) #YoY for previous year
    st.metric(label='YOY GROWTH', value = "{}%".format(millify(yoy_growth, 2)), 
    delta = "{}%".format(millify(int(yoy_growth - yoy_growth_last_year), 2)),
    help = 'Year over Year Growth')

with col41:
    st.metric(label='Target', value = "$2M", delta= -12, help = 'Target for this year compared to that of last year')


# SECOND HORIZONTAL BAR AT THE HOME PAGE [TARGET FOR THIS YEAR]
st.markdown("---")

# Target this year
target_sales = 80000
current_sales = 30000
delta = target_sales - current_sales
values = [current_sales, delta]
colors = ["#e05628", "#C7C9CE"]
fig_target_sales = go.Figure(data = go.Pie(values = values, hole = 0.8, marker_colors = colors))
fig_target_sales.update_traces(hoverinfo='value+percent', 
    textinfo = 'none',
    # textfont_size=20, 
    rotation= 45, 
    showlegend = False,)

fig_target_sales.add_annotation(x= 0.5, y = 0.5,
                        text = '${}'.format(millify(target_sales)),
                        font = dict(size = 50,family='sana serif', 
                                    color='gray'),
                        showarrow = False)
fig_target_sales.update_layout(
    title_text = '<b>Target for this year</b>',
    )


# filter options
sales_by_product_category = sales_df.query("year == @this_year").groupby(by=['product_category_name_english']).sum()['payment_value'].sort_values(ascending=True)[:10]
fig_product_sales = px.bar(sales_by_product_category,
            x="payment_value",
            y = sales_by_product_category.index,
            title="<b>Sales by Product Category (Top Ten)</b>",
            orientation='h',
            color_discrete_sequence=["#e05628"],
            template="plotly_white"
        )
order_status_plot = sales_df.query("year == 2018")['order_status']

# NEW ROW [1X2]
st.subheader('Revenue Forcast')
col_empty1, col12, col22, col_empty2 = st.columns([1,5,5,1], gap='small')
with col_empty1:
    st.empty()
with col12:
    st.plotly_chart(fig_target_sales, use_container_width=True)

with col22:
    fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False)))
    st.plotly_chart(fig_product_sales, use_container_width=False)

with col_empty2:
    st.empty()


# EXPERIMENT
fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False)))
st.plotly_chart(fig_product_sales, use_container_width=True)
# with col22:
#     st.plotly_chart(fig_order_status)

if show_df:
    st.dataframe(sales_df)

# st.columns()