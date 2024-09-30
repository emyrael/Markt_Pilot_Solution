# Mart Pilot Data Engineering Challenge

## Overview

This repository contains my solution to the data engineering coding challenge for Mart Pilot. The goal of this challenge is to design and implement an ETL pipeline that processes anonymized sample data stored in MongoDB collections, transforming it into a relational structure suitable for analytics.

## Files and Directories

- **Data Exploration**: The data exploration is documented in `data_exploration.ipynb`.
- **ETL Script**: The ETL process is implemented in `etl_script.py`.
- **Dependencies**: The Docker file contains the necessary dependencies to run the project.


## Challenge Objective

The task is to build an ETL/ELT pipeline in Python that extracts data from the given MongoDB collections, transforms the data into a relational schema, and loads it into a PostgreSQL database. The pipeline answers key analytical questions such as:

- How many results are there per part, shop, country, and customer?
- How have prices per part evolved over time?

## Data Description

The data consists of four collections in JSON format:

- **clients**: Information about our clients.
- **suppliers**: Information about web shops where pricing data is sourced.
- **sonar_runs**: Records of price research operations performed by Sonar (a scraping tool).
- **sonar_results**: Detailed pricing information for a specific part in a specific shop.

## Solution Components

### 1. Data Extraction
- The pipeline reads JSON files representing MongoDB collections  to fetch data.

### 2. Data Transformation
- The pipeline processes and cleans the data while maintaining referential integrity between entities.
- The transformed data is optimized for answering key analytical questions such as part pricing trends and supplier information.

### 3. Data Loading
- The transformed data is loaded into a PostgreSQL database, structured to facilitate complex queries and analysis.

## Key Features

- **Schema Design**: A well-defined relational schema is created to accommodate the transformed data while preserving key relationships between entities.
- **Referential Integrity**: The solution ensures that relationships between clients, suppliers, and price results are maintained in the relational database.
- **Query Optimization**: The schema design supports efficient querying for pricing trends and part availability.

## How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/emyrael/Markt_Pilot_Solution.git
    ```

2. Build and Run the Container
    ```bash
   docker-compose up --build

    ```


## Deployment Strategy

In a production environment, I would:

- Use Docker to containerize the application for portability and consistency.
- Utilize Infrastructure as Code (IaC) tools (like Terraform) for managing cloud resources.
- Implement CI/CD pipelines using GitHub Actions or Jenkins for automated testing and deployment.
- Monitor the pipeline using logging (e.g., ELK Stack) and alerts for failures or performance bottlenecks.

## Documentation

- Detailed transformation steps and assumptions made during development are documented in the `docs/` folder.



