# -*- coding: utf-8 -*-

import json
import ujson as json2
import pandas as pd
from sqlalchemy import create_engine

# Loading the JSON files
with open('collections/clients.json') as f:
    clients = json.load(f)

with open('collections/suppliers.json') as f:
    suppliers = json.load(f)

with open('collections/sonar_runs.json') as f:
    sonar_runs = json.load(f)

with open('collections/sonar_results.json') as f:
    sonar_results = json2.load(f)


# Converting thr files to Pandas DataFrames for easier manipulation
clients_df = pd.json_normalize(clients)
suppliers_df = pd.json_normalize(suppliers)
sonar_runs_df = pd.json_normalize(sonar_runs)
sonar_results_df = pd.json_normalize(sonar_results)


# Transforming the data to relevant format to allow easier manipulation


# Rename '_id.$oid' to 'supplier_id' in suppliers_df for easier merging
suppliers_df.rename(columns={'_id.$oid': 'supplier_id'}, inplace=True)

# Rename 'supplier_id.$oid' in sonar_results_df to match with suppliers_df
sonar_results_df.rename(columns={'supplier_id.$oid': 'supplier_id'}, inplace=True)

# Now we can join sonar_results with suppliers on 'supplier_id'
merged_results_suppliers = sonar_results_df.merge(suppliers_df, on='supplier_id', how='inner')


# Now group by part_id and supplier to count results per part and shop
results_per_part_shop = merged_results_suppliers.groupby(['part_id.$oid', 'name']).size().reset_index(name='results_count')


# Join sonar_results with sonar_runs to answer "How did prices per part develop over time?"
# First, rename 'sonar_run_id.$oid' in sonar_results_df and '_id.$oid' in sonar_runs_df for consistency
sonar_results_df.rename(columns={'sonar_run_id.$oid': 'sonar_run_id'}, inplace=True)
sonar_runs_df.rename(columns={'_id.$oid': 'sonar_run_id'}, inplace=True)

# Join sonar_results with sonar_runs to include the 'run_date'
merged_results_runs = sonar_results_df.merge(sonar_runs_df, on='sonar_run_id', how='inner')


# Select relevant columns for price trends (part_id, price, run_date)
price_trends = merged_results_runs[['part_id.$oid', 'price_norm', 'date.$date']]


# Convertimg run_date to datetime for time-based analysis
price_trends['date.$date'] = pd.to_datetime(price_trends['date.$date'])

# Add 'month' and 'year' columns for filtering
price_trends['month'] = price_trends['date.$date'].dt.month
price_trends['year'] = price_trends['date.$date'].dt.year

# Group by part_id and resample by run_date to get average price per month
price_trends_grouped = price_trends.groupby('part_id.$oid').resample('M', on='date.$date').mean().reset_index()


# Joining and renaming '_id.$oid' in clients_df to 'client_id' and 'client_id.$oid' in sonar_runs_df to 'client_id'
clients_df.rename(columns={'_id.$oid': 'client_id'}, inplace=True)
sonar_runs_df.rename(columns={'client_id.$oid': 'client_id'}, inplace=True)

# List of columns to select from sonar_runs_df
columns_to_select = [
    'category', 'status', 'countries', 'proxy_country', 'created_parts_count',
    'published_parts_count', 'only_already_found', 'sonar_run_type', 'use_proxy',
    'total_sonar_results_count', 'search_login_pages', 'sonar_run_id', 'date.$date', 'time.$date'
]

# Perform a left join on 'client_id'
merged_df_client = clients_df.merge(sonar_runs_df[columns_to_select + ['client_id']],
                             on='client_id',
                             how='left')


# Total count of sonar runs per client
sonar_run_count_per_client = merged_df_client.groupby('client_id').size().reset_index(name='sonar_run_count')

# Average number of created and published parts per client
average_parts_per_client = merged_df_client.groupby('client_id').agg({
    'created_parts_count': 'mean',
    'published_parts_count': 'mean'
}).reset_index().rename(columns={
    'created_parts_count': 'average_created_parts',
    'published_parts_count': 'average_published_parts'
})

# Statuses of sonar runs per category
status_per_category = merged_df_client.groupby(['category', 'status']).size().reset_index(name='count')

print("Total Count of Sonar Runs per Client:")
print(sonar_run_count_per_client)

print("\nAverage Number of Created and Published Parts per Client:")
print(average_parts_per_client)

print("\nStatuses of Sonar Runs per Category:")
print(status_per_category)


# **Loading the transformed data into a new PostgreSQL DB**
# Database connection setup
engine = create_engine('postgresql://postgres:emyrael@db:5432/markt_pilot')


# Load the new dataframe into PostgreSQL
price_trends_grouped.to_sql('price_trends', engine, if_exists='replace', index=False)
merged_df_client.to_sql('sonar_runs_client', engine, if_exists='replace', index=False)