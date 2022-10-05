# import required libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from millify import millify

# Page configurations
st.set_page_config(
    page_title = 'KPI Dashboard',
    page_icon = "📈",
    layout = 'wide',


)

# ---------CUSTOM STYLE BEGINS--------------
padding_top = 0
custom_style = """
            <style>
            .appview-container{
                padding-top: {padding_top}rem;
            }
            footer {visibility: hidden;}
            </style>
"""
st.markdown(custom_style, unsafe_allow_html=True)

# ---------CUSTOM STYLE ENDS--------------

# Load Data
# @st.cache
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

    start_time = st.slider(label="Select Date Range", 
    min_value = datetime(sales_df.year.min(), sales_df.month.min(), 1), 
    max_value = datetime(sales_df.year.max(), sales_df.month.max(), 1), 
    value = [datetime(sales_df.year.max(), 1, 1), datetime(sales_df.year.max(), 12, 31)], 
    format="MM-YY")
    order_status = st.multiselect(label="Order Status", 
    options=sales_df.order_status.unique(),
    default = "Delivered")

    # more_filter_options = st.checkbox(label="Apply More Filters", value=False)


with st.sidebar:
    filter_by_state = st.multiselect(label = "Add State",
    options=sales_df.customer_state.unique(),
    key=1)

    filter_by_product_line = st.multiselect(label = "Product Category",
    options=sales_df.product_category_name_english.unique(), 
    key=2)
filtered_df = sales_df.query(
    "customer_state == @filter_by_state & product_category_name_english == @filter_by_product_line")

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

# Average star rating
def average_star_rating():
    star_rating = sales_df.query("order_status == 'Delivered'").query("year == @this_year")['review_score'].astype('float64').mean()
    return round(star_rating, 1)

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
    delta= "${}".format(millify(total_canceled_order - total_canceled_order_last_year)),
    help = 'Value of orders that were canceled this year, compared to last year',
    delta_color="inverse",
    )

with col31:
    yoy_growth = YoY_growth(this_year, last_year)
    yoy_growth_last_year = YoY_growth(last_year, last_year-1) #YoY for previous year
    st.metric(label='YOY GROWTH', value = "{}%".format(millify(yoy_growth, 2)), 
    delta = "{}%".format(millify(int(yoy_growth - yoy_growth_last_year), 2)),
    help = 'Percentage of revenue growth this year, compared to this time last year')

with col41:
    star_rating_value = average_star_rating()
    st.write("AVERAGE RATING")
    st.metric(label='{}'.format('⭐'*int(star_rating_value)), value = "{}".format(star_rating_value), help = 'Average star rating from customers whose orders have been delivered to them this year')


# SECOND HORIZONTAL BAR AT THE HOME PAGE [TARGET FOR THIS YEAR]
st.markdown("---")
# Target this year
target_sales = 11000000
current_sales = 4000000
delta = target_sales - current_sales
values = [current_sales, delta]
colors = ["#e05628", "#C7C9CE"]
fig_target_sales = go.Figure(data = go.Pie(values = values, hole = 0.75, marker_colors = colors, domain = {'x': [0,1], 'y': [0,1]},),
layout={'height': 500, 'width' : 500,},)
fig_target_sales.update_traces(hoverinfo='value+percent', textinfo = 'none', rotation= 45, showlegend = False,)
fig_target_sales.add_annotation(x= 0.5, y = 0.5,
                        text = '${}'.format(millify(target_sales)),
                        font = dict(size = 30,family='sans serif',),
                        showarrow = False)

# TEAM GOALS
def plot_team_goals(team_name, target_revenue = 5000000, current_revenue = 500000):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        number = {'prefix': "$", 'font': {'size': 18}},
        value = target_revenue,
        title = {'text': team_name, 'font': {'size': 14}},
        align = 'center',
        domain = {'x': [0,1], 'y': [0,1]},
        gauge = {
            'shape': "bullet",
            'axis': {'ticks': "", 'showticklabels': False,},
            'bar': {'color': "rgba(0,0,0,0)", 'thickness': 0.3,},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps' : [{'range': [0, current_revenue], 'color': "#e05628"},
            {'range': [current_revenue, target_revenue], 'color': "#C7C9CE"}],
            },
            ))
    fig.update_layout(autosize = True,
                    height = 50,
                    # width = 500,
                    margin = dict(r=0, b=0.2, t=0.2)
                    )
    return fig                 

# filter options
sales_by_product_line = sales_df.query("year == @this_year").groupby(by=['product_category_name_english']).sum()['payment_value'].sort_values(ascending=True)[:10]
fig_product_sales = px.bar(
    data_frame = sales_by_product_line,
    x="payment_value",
    y = sales_by_product_line.index,
    title="<b>Sales by Product Line</b>",
    orientation='h',
    color_discrete_sequence=["#e05628"],
    template="plotly_white"
        )

sales_by_region = sales_df.query("year == @this_year").query("order_status == 'Delivered'").groupby('customer_state').sum()['payment_value'].sort_values(ascending=False)[:10]
fig_sales_by_region = px.bar(
    data_frame = sales_by_region,
    y="payment_value",
    x=sales_by_region.index,
    title="<b>Sales by Region</b>",
    orientation='v',
    color_discrete_sequence=["#e05628"],
    template="plotly_white"
)
# NEW ROW [1X2]
st.subheader('Revenue Forcast')
col12, col22 = st.columns([3,5], gap='medium')
# with col_empty1:
#     st.empty()
with col12:
    # st.markdown("##### Target For This Year", unsafe_allow_html=True)
    fig_target_sales.update_layout(
        title = {'text': 'Target For This Year', 'font': {'size': 18}, 'x':0, 'y':1},
        autosize = False, height=400, width=400, plot_bgcolor = "rgba(0,0,0,0)", xaxis = (dict(showgrid=False)))
    st.plotly_chart(fig_target_sales, use_container_width=True)

with col22:
    st.markdown("###### Team Goals", unsafe_allow_html=True)
    marketing = plot_team_goals(team_name='Marketing', target_revenue=3000000, current_revenue=1500000)
    st.plotly_chart(marketing)
    sales = plot_team_goals(team_name="Sales", target_revenue = 7000000, current_revenue=5000000)
    st.plotly_chart(sales)
    operations = plot_team_goals(team_name='Operations', target_revenue=2000000, current_revenue=1700000)
    st.plotly_chart(operations)

# with col_empty2:
#     st.empty()

st.markdown("---")
st.subheader('Top Tens')
dist_col1, dist_col2 = st.columns(2)
with dist_col1:
    fig_product_sales.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = (dict(showgrid=False)))
    st.plotly_chart(fig_product_sales, use_container_width=True)

with dist_col2:
    fig_sales_by_region.update_layout(
        plot_bgcolor = "rgba(0,0,0,0)",
        xaxis = (dict(showgrid=False)))
    st.plotly_chart(fig_sales_by_region, use_container_width=True)

if show_df:
    st.dataframe(sales_df)