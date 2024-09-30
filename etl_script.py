# -*- coding: utf-8 -*-
import json
import ujson as json2
import pandas as pd
from sqlalchemy import create_engine

# Function to extract data from JSON files
def extract():
    with open('collections/clients.json') as f:
        clients = json.load(f)

    with open('collections/suppliers.json') as f:
        suppliers = json.load(f)

    with open('collections/sonar_runs.json') as f:
        sonar_runs = json.load(f)

    with open('collections/sonar_results.json') as f:
        sonar_results = json2.load(f)

    return clients, suppliers, sonar_runs, sonar_results

# Function to transform the data into Pandas DataFrames and perform necessary transformations
def transform(clients, suppliers, sonar_runs, sonar_results):
    # Converting the files to Pandas DataFrames
    clients_df = pd.json_normalize(clients)
    suppliers_df = pd.json_normalize(suppliers)
    sonar_runs_df = pd.json_normalize(sonar_runs)
    sonar_results_df = pd.json_normalize(sonar_results)

    # Rename columns for consistency and easier merging
    suppliers_df.rename(columns={'_id.$oid': 'supplier_id'}, inplace=True)
    sonar_results_df.rename(columns={'supplier_id.$oid': 'supplier_id'}, inplace=True)
    
    # Merging sonar results with suppliers
    merged_results_suppliers = sonar_results_df.merge(suppliers_df, on='supplier_id', how='inner')

    # Group by part_id and supplier to count results per part and shop
    results_per_part_shop = merged_results_suppliers.groupby(['part_id.$oid', 'name']).size().reset_index(name='results_count')

    # Joining sonar results with sonar runs
    sonar_results_df.rename(columns={'sonar_run_id.$oid': 'sonar_run_id'}, inplace=True)
    sonar_runs_df.rename(columns={'_id.$oid': 'sonar_run_id'}, inplace=True)
    merged_results_runs = sonar_results_df.merge(sonar_runs_df, on='sonar_run_id', how='inner')

    # Selecting relevant columns for price trends
    price_trends = merged_results_runs[['part_id.$oid', 'price_norm', 'date.$date']]
    
    # Converting run_date to datetime for time-based analysis
    price_trends['date.$date'] = pd.to_datetime(price_trends['date.$date'])
    price_trends['month'] = price_trends['date.$date'].dt.month
    price_trends['year'] = price_trends['date.$date'].dt.year
    
    # Group by part_id and resample by run_date to get average price per month
    price_trends_grouped = price_trends.groupby('part_id.$oid').resample('M', on='date.$date').mean().reset_index()

    # Renaming columns in clients and sonar_runs for merging
    clients_df.rename(columns={'_id.$oid': 'client_id'}, inplace=True)
    sonar_runs_df.rename(columns={'client_id.$oid': 'client_id'}, inplace=True)
    
    # List of columns to select from sonar_runs_df
    columns_to_select = [
        'category', 'status', 'countries', 'proxy_country', 'created_parts_count',
        'published_parts_count', 'only_already_found', 'sonar_run_type', 'use_proxy',
        'total_sonar_results_count', 'search_login_pages', 'sonar_run_id', 'date.$date', 'time.$date'
    ]
    
    # Perform a left join on 'client_id'
    merged_df_client = clients_df.merge(sonar_runs_df[columns_to_select + ['client_id']], on='client_id', how='left')

    return merged_results_runs, merged_results_suppliers, price_trends_grouped, merged_df_client

# Function to load the transformed data into a PostgreSQL database
def load(merged_results_runs, merged_results_suppliers, price_trends_grouped, merged_df_client):
    # Database connection setup
    engine = create_engine('postgresql://postgres:emyrael@db:5432/markt_pilot')

    # Loading data into PostgreSQL
    #merged_results_runs.to_sql('merged_results_runs', engine, if_exists='replace', index=False)
    #merged_results_suppliers.to_sql('merged_results_suppliers', engine, if_exists='replace', index=False)
    price_trends_grouped.to_sql('price_trends_grouped', engine, if_exists='replace', index=False)
    merged_df_client.to_sql('merged_df_client', engine, if_exists='replace', index=False)

# Main function to execute the ETL pipeline
def main():
    # Step 1: Extract data from JSON files
    clients, suppliers, sonar_runs, sonar_results = extract()

    # Step 2: Transform the data
    merged_results_runs, merged_results_suppliers, price_trends_grouped, merged_df_client = transform(clients, suppliers, sonar_runs, sonar_results)

    # Step 3: Load the data into PostgreSQL
    load(merged_results_runs, merged_results_suppliers, price_trends_grouped, merged_df_client)

if __name__ == "__main__":
    main()
