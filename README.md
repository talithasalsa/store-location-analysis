# New Store Location Analysis
---

## Project Overview
This project utilized ETL data processing. Main objectives are to analyze and decide the new store location based on sales record and business expenses. The analysis concluded the most optimum new store location and provided further business recommendation.

---

## ETL Workflow

**1. Extract Data**
- Original data was retrieved from [Kaggle](https://www.kaggle.com/datasets/dsfelix/us-stores-sales/code) and stored in PostgreSQL
- Extract data from PostgreSQL using Python

**2. Transform Data**
- Clean data (delete duplicates, normalized columns)
- Store clean data in a CSV file

**3. Load Data**
- Use Apache Airflow to schedule and manage loading tasks
- Load data to ElasticSearch

**4. Visualize Data**
- Data is visualize using Kibana
