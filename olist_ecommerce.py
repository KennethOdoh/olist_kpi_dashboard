#!/usr/bin/env python
# coding: utf-8

# ## Attention
# 
# An order might have multiple items.
# 
# Each item might be fulfiled by a distinct seller

# In[1]:


#Import required libraries
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
# import streamlit as st
# import plotly


# In[ ]:





# In[2]:


# The datasets were combined into one Excel file with multiple sheets
#Load workbook
xl = pd.ExcelFile('olist_store_dataset.xlsx', engine='openpyxl')


# In[3]:


# list of sheets containing the datasets
xl.sheet_names


# ### Load the tables from Excel worksheet to a pandas dataframe

# In[4]:


# Customers data sheet
customers_df = pd.read_excel(xl, sheet_name='customers_data')
customers_df.head(2)


# In[7]:


customers_df.info()


# In[8]:


# change column datatypes
convert_dict = {
    'customer_zip_code_prefix': str,
    'customer_city': 'category',
    'customer_state': 'category',
}
customers_df = customers_df.astype(convert_dict)

# Let's standardize customer_zip_code_prefix digits to 5 for the column
customers_df.customer_zip_code_prefix = customers_df.customer_zip_code_prefix.str.zfill(5)

customers_df.info()


# In[30]:


customers_df.customer_zip_code_prefix.sample(5)


# In[31]:


# geolocation data sheet
geolocation_df = pd.read_excel(xl, sheet_name='geolocation_data')
geolocation_df


# In[32]:


geolocation_df.info()


# In[33]:


# Change data types of listed columns
convert_dict = {
    'geolocation_zip_code_prefix' : str,
    'geolocation_city': 'category',
    'geolocation_state': 'category',
}
geolocation_df = geolocation_df.astype(convert_dict)


# Let's standardize geolocation_zip_code_prefix digits to 5 for the column
geolocation_df.geolocation_zip_code_prefix = geolocation_df.geolocation_zip_code_prefix.str.zfill(5)


# In[34]:


geolocation_df.info()


# In[35]:


geolocation_df.geolocation_zip_code_prefix.sample(10)


# In[36]:


# order_items data sheet
order_items_df = pd.read_excel(xl, sheet_name='order_items_data')
order_items_df.head(2)


# In[37]:


order_items_df.info()


# - Change datatypes for some columns
# - Drop the shipping_limit_date column

# In[38]:


convert_dict = {
    'order_item_id': str,
    'product_id': str,
    'seller_id': str,    
}

order_items_df = order_items_df.astype(convert_dict)
order_items_df = order_items_df.drop(columns=['shipping_limit_date'])


# In[39]:


order_items_df.info()


# In[40]:


# order_payments data sheet
order_payments_df = pd.read_excel(xl, sheet_name='order_payments_data')
order_payments_df.head(2)


# In[41]:


order_payments_df.info()


# In[42]:


order_payments_df.duplicated().any()


# In[43]:


# order_payments_df contains duplicate rows
order_payments_df[order_payments_df.duplicated()]


# In[44]:


# Change datatype
convert_dict = {
    'order_id': str,
    'payment_type': 'category', 
}
order_payments_df = order_payments_df.astype(convert_dict)

# drop irrelevant columns
order_payments_df = order_payments_df.drop(columns=['payment_sequential', 'payment_installments'])
order_payments_df.info()

# drop duplicates
order_payments_df = order_payments_df.drop_duplicates()


# In[45]:


order_payments_df.duplicated().any()


# In[46]:


# order_reviews data sheet
order_reviews_df = pd.read_excel(xl, sheet_name='order_reviews_data')
order_reviews_df.head(2)


# In[47]:


order_reviews_df.info()


# In[48]:


# change dtype
convert_dict = {
    'review_score': 'category',
}
order_reviews_df = order_reviews_df.astype(convert_dict)

# drop irrelevant columns
order_reviews_df = order_reviews_df.drop(columns=['review_creation_date','review_comment_message',
                                                  'review_comment_title','review_answer_timestamp',
                                                 ])
order_reviews_df.info()


# In[49]:


# orders data sheet
orders_df = pd.read_excel(xl, sheet_name='orders_data')
orders_df.head(2)


# In[50]:


orders_df.info()


# In[51]:


# change dtype
orders_df["order_status"] = orders_df.order_status.astype('category')

# drop irrelevant columns
orders_df = orders_df.drop(columns = ['order_delivered_carrier_date', 
                                      'order_estimated_delivery_date'
                                     ])
orders_df.info()


# In[52]:


# products data sheet
products_df = pd.read_excel(xl, sheet_name='products_data')
products_df.head(2)


# In[53]:


products_df.info()


# In[54]:


# drop irrelevant columns
products_df = products_df.drop(columns=['product_name_lenght',
       'product_description_lenght', 'product_photos_qty', 'product_weight_g',
       'product_length_cm', 'product_height_cm', 'product_width_cm'])
products_df.info()


# In[55]:


# sellers data sheet
sellers_df = pd.read_excel(xl, sheet_name='sellers_data')
sellers_df.sample(10)


# In[56]:


sellers_df.info()


# In[57]:


# change data types of columns
convert_dict = {
    'seller_zip_code_prefix': str,
    'seller_id': str,
    'seller_city': 'category',
    'seller_state': 'category',
}
sellers_df = sellers_df.astype(convert_dict)

# Let's standardize seller_zip_code_prefix digits to 5 for the column
sellers_df.seller_zip_code_prefix = sellers_df.seller_zip_code_prefix.str.zfill(5)

sellers_df.info()


# In[58]:


# product_categories data sheet
product_categories_df = pd.read_excel(xl, sheet_name='product_categories_data')
product_categories_df


# ## Using the schema below, let's merge the tables.
# 
# >1.	An order might have multiple items.
# 2.	Each item might be fulfilled by a distinct seller.
# 3.	All text identifying stores and partners were replaced by the names of Game of Thrones great houses.
# 

# <img src='schema.png' alt='Table schema' width='750px'>

# In[59]:


#  orders_df + order_reviews = orders
orders = pd.merge(orders_df, order_reviews_df, on='order_id', how='left')
orders.info()


# In[60]:


orders.duplicated().any()


# In[61]:


# orders + order_payments_df = orders
orders = pd.merge(orders, order_payments_df, on='order_id', how='left')
orders.info()


# In[62]:


order_payments_df.query("order_id == '8ca5bdac5ebe8f2d6fc9171d5ebc906a'")


# In[63]:


# orders + order_items_df = orders
orders = pd.merge(orders, order_items_df, on='order_id', how='left')
orders.info()


# In[64]:


# orders + products = orders
orders = pd.merge(orders, products_df, on='product_id', how='left')
orders.info()


# In[65]:


# orders + sellers_df = orders
orders = pd.merge(orders, sellers_df, on='seller_id', how='left')
orders.info()


# ### Fetch Seller Latitude and Longitude values from the geolocation table

# In[43]:


# orders['seller_lat'] = pd.merge(orders, geolocation_df, 
#                                         left_on=['seller_zip_code_prefix', 'seller_state', 'seller_city'], 
#                                         right_on=['geolocation_zip_code_prefix', 'geolocation_state', 'geolocation_city'], 
#                                          how='left')['geolocation_lat']


# In[ ]:


# orders['seller_lng'] = pd.merge(orders, geolocation_df, 
#                                          left_on=['seller_zip_code_prefix', 'seller_state', 'seller_city'], 
#                                          right_on=['geolocation_zip_code_prefix', 'geolocation_state', 'geolocation_city'], 
#                                          how='left')['geolocation_lng']


# In[83]:


orders_copy = orders.copy()


# In[98]:


# EXPERIMENTAL

# Convert columns to string, then combine to form a new id column

geolocation_df['geo_multikey'] = geolocation_df['geolocation_zip_code_prefix'] + "" + geolocation_df['geolocation_state'].astype(str).replace(' ', '') + "" + geolocation_df['geolocation_city'].astype(str).replace(' ', '')  #+"" #.str.replace('\n', '')
orders_copy['seller_multikey'] = orders_copy['seller_zip_code_prefix'] + "" + orders_copy['seller_state'].astype(str).replace(' ', '') + "" + orders_copy['seller_city'].astype(str).replace(' ', '')


# In[ ]:


orders_copy['seller_lat'] = pd.merge(orders_copy, geolocation_df, left_on='seller_multikey', right_on='geo_multikey', how='left')['geolocation_lat']
orders_copy['seller_lng'] = pd.merge(orders_copy, geolocation_df, left_on='seller_multikey', right_on='geo_multikey', how='left')['geolocation_lng']


# In[87]:


orders_copy['seller_lng'].value_counts(dropna=False)


# In[102]:


geolocation_df['geo_multikey']


# In[100]:


orders_copy['seller_multikey']


# In[45]:


orders


# ### Also, fetch Customer Latitude and Longitude values from the geolocation table

# In[46]:


customers_df['customer_lat'] = pd.merge(customers_df, geolocation_df, 
                                         left_on=['customer_zip_code_prefix', 'customer_state', 'customer_city'], right_on=['geolocation_zip_code_prefix', 'geolocation_state', 'geolocation_city'], 
                                         how='left')['geolocation_lat']


# In[47]:


customers_df['customer_lng'] = pd.merge(customers_df, geolocation_df, 
                                         left_on=['customer_zip_code_prefix', 'customer_state', 'customer_city'], right_on=['geolocation_zip_code_prefix', 'geolocation_state', 'geolocation_city'], 
                                         how='left')['geolocation_lng']


# In[ ]:


customers_df['customer_multikey'] = customers_df['customer_zip_code_prefix'] + str(customers_df['customer_state']) + str(customers_df['customer_city'])
customers_df['customer_lat'] = pd.merge(orders, geolocation_df, left_on='customer_multikey', right_on = 'geo_multikey')['geolocation_lat']
customers_df['customer_lng'] = pd.merge(orders, geolocation_df, left_on='customer_multikey', right_on = 'geo_multikey')['geolocation_lng']


# In[48]:


customers_df


# ### Finally, merge customers_df with orders using customer_id column

# In[49]:


# orders + customers_df = sales_df
sales_df = pd.merge(orders, customers_df, on = 'customer_id', how='right')
sales_df


# ### Copy the sales_df table for further cleaning

# In[50]:


sales_df_clean = sales_df.copy()
sales_df_clean


# In[51]:


# Export to csv for visual cleaning
sales_df_clean.to_csv('dirty_sales_data.csv', index=False)


# In[52]:


sales_df_clean.info()


# In[53]:


sales_df_clean.describe()


# ### Additional Data Quality Issues
# - Product category column not in English
# - '_' in item and category names
# - City names are in lower case

# In[ ]:





# ### Product category column not in English
# 
# Replace product category name column with the translated one in the products_category_translation csv file

# In[54]:


sales_df_clean.product_category_name.sample(15)


# In[55]:


for i in sales_df_clean.product_category_name:
    assert (str(i).islower())


# In[56]:


# Some products categories were not translated to English, while others are not available
print(sales_df_clean.product_category_name.nunique(dropna=False))
print(product_categories_df.product_category_name.nunique(dropna=False))


# In[57]:


missing_cat = {'product_category_name' : ['portateis_cozinha_e_preparadores_de_alimentos', 'pc_gamer', np.nan],
    'product_category_name_english' : ['Kitchen Equipment', 'PC Gamer', 'Not Available']}

df = pd.DataFrame(data=missing_cat)

# Concatenate with the product_categories_df dataframe
product_categories_df = pd.concat([product_categories_df, df], ignore_index=True)
product_categories_df


# In[58]:


# Next, replace the Portugese category names to English version
sales_df_clean = sales_df_clean.replace(sales_df_clean.product_category_name.unique(), product_categories_df.product_category_name_english.unique())
sales_df_clean.product_category_name.unique()


# ### '_' in item and category names
# 
# ### City names are in lower case
# 
# Replace all underscores in named columns of the Dataframe to have a cleaner data, then, convert to title case

# In[59]:


sales_df_clean.customer_city


# In[60]:


# Replace all underscores with white space
named_columns = ['order_status', 'payment_type', 'product_category_name', 'seller_city', 'customer_city',]
sales_df_clean[named_columns] = sales_df_clean[named_columns].astype(str)
sales_df_clean[named_columns] = sales_df_clean[named_columns].replace('_', ' ', regex=True)

# Next, convert to title case
for col in named_columns:
    sales_df_clean[col] = sales_df_clean[col].str.title()


# In[61]:


sales_df_clean[named_columns].info()


# In[62]:


# Re-convert columns to desired datatypes

ordered_category ={
    'order_status': ['Unavailable', 'Created', 'Invoiced', 'Approved', 'Processing', 'Shipped', 'Canceled', 'Delivered',],
    'review_score': [1, 2, 3, 4, 5],
    'payment_type': ['Credit Card', 'Debit Card', 'Voucher', 'Boleto', 'Not Defined', 'Nan'],    
    }

# Convert to categorical datatype
for category in ordered_category:
    ordered_var = pd.api.types.CategoricalDtype(categories=ordered_category[category], 
                                                ordered = True)
    sales_df_clean[category] = sales_df_clean[category].astype(ordered_var)
    
    
# Convert other columns to unordered categories
sales_df_clean['product_category_name'] = sales_df_clean['product_category_name'].astype('category')


# In[63]:


sales_df_clean.info()


# In[329]:


# OPTIONAL
# Now, let's export our cleaned data

sales_df_clean.to_csv('cleaned_sales_data.csv', index=False)


# In[64]:



sales_df_clean.order_status.unique()


# # UNIVARIATE ANALYSIS

# In[65]:


sales_df_clean.info()


# In[ ]:





# In[66]:


# Distribution of variables
sales_df_clean.order_id.nunique()


# Total unique customers till date

# In[67]:


sales_df_clean.customer_unique_id.nunique()


# In[ ]:


sales_df_clean[]


# ### 1: Sales Volume by location

# In[ ]:





# In[ ]:




