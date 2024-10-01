# ETL Pipeline for Data Processing

This repository contains an ETL (Extract, Transform, Load) pipeline designed for efficient data extraction, transformation, and loading into a Postgres database. The setup uses Docker for containerization, ensuring easy setup and environment consistency.

---

## Overview

The primary purpose of this project is to streamline data processing using an ETL pipeline. This pipeline automates the following tasks:
- **Extracting** data from external sources.
- **Transforming** the extracted data to meet specific analytical or business needs.
- **Loading** the transformed data into a PostgreSQL database for easy analysis and further data processing.

This project leverages **Docker** for containerization to simplify deployment and ensure consistency across different environments. Docker allows this pipeline to run seamlessly on any system that supports Docker, ensuring compatibility and ease of use across different development environments.

---

## Project Structure

The repository contains the following key files:

```bash
.
├── Dockerfile                 # Docker configuration for setting up the environment
├── docker-compose.yml         # Docker Compose file for setting up services (Postgres, ETL script)
├── etl_script.py              # Main Python script for the ETL process
├── requirements.txt           # Python dependencies for the ETL script
├── data_exploration.ipynb     # Jupyter notebook for initial data exploration and insights

```

ETL Process
The ETL script (etl_script.py) handles the following:

- **Extract** Data is extracted from external sources.
- **Transform** The extracted data undergoes necessary transformations. If more time was available, further improvements could be made, such as modifying the column names for better readability and easier data joins.
- **Load** The transformed data is loaded into a PostgreSQL database.

## Strengths of the Approach
Dockerization: The use of Docker ensures that the pipeline can run on any system without worrying about dependency or environment conflicts. This enhances the compatibility and flexibility of the solution across various environments.
Data Exploration
In the data_exploration.ipynb notebook, some initial insights were drawn from the data. For example:

The number of suppliers by country was examined.
A quick analysis of the number of results per data set was performed.
These basic insights helped ensure the integrity of the data and provided context for more in-depth analysis during the transformation phase of the ETL process.
