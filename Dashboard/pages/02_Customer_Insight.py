import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from Home import load_data

sales_df = st.dataframe(load_data('../cleaned_sales_data.csv'))