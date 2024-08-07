'''
MILESTONE 3

Nama  : Talitha Salsabila
Batch : RMT-032

Project ini berisi program automatisasi pengolahan dan transfer data dari PostgreSQL ke ElasticSearch.
Dataset yang digunakan berupa data penjualan suatu toko di US dalam 1 tahun.

'''
# Import libraries

import pandas as pd
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from elasticsearch import Elasticsearch

import datetime as dt
from datetime import timedelta
import psycopg2 as db


# Fetch data from postgres
def fetch_data(): 

    '''
    Fungsi ini bertujuan untuk mengambil data dari PostgreSQL yang kemuadian akan dilakukan data cleaning.

    Parameters:
    dbname: nama database dimana data disimpan 
    user: instansi yang mengakses database PostgreSQL
    table_m3: nama dataset PostgreSQL yang akan diambil

    '''

    conn_string="dbname='airflow' host='postgres' user='airflow' password='airflow' port='5432'"
    conn=db.connect(conn_string)
    df=pd.read_sql("select * from table_m3", conn)
    df.to_csv('/opt/airflow/dags/P2M3_talitha_salsabila_data_raw.csv', sep=',', index=False)

    conn.close()

# Clean data
def clean_data():

    '''
    Fungsi ini bertujuan untuk cleaning data yang telah terambil dari PostgreSQL.
    Jenis cleaning yang dilakukan ialah menghilangkan duplikat data, menggantu uppercase menjadi lowercase,
    menghilangkan spasi pada judul kolom, mengisi missing value dengan teknik forward fill.
    Data kemudian disimpan pada folder dags dengan nama 'P2M3_talitha_salsabila_data_clean.csv'. 
    
    '''
    df = pd.read_csv('/opt/airflow/dags/P2M3_talitha_salsabila_data_raw.csv') # read csv data
    df.drop_duplicates(inplace=True)                                        # drop duplicated data
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]      # change uppercase to lowercase & change sapce to underscore
    # df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')              # change object datatype to datetime
    df.fillna(method='ffill', inplace=True)                                 # impute missing values with forward fill

    df.to_csv('/opt/airflow/dags/P2M3_talitha_salsabila_data_clean.csv', index=False)    # save cleaned data


# Load data to Elasticsearch

'''
Fungsi ini dibuat untuk mengunggah data yang telah dibersihkan ke ElasticSearch. 

'''
def load_to_elasticsearch():
    es = Elasticsearch("http://elasticsearch:9200") 
    df = pd.read_csv('/opt/airflow/dags/P2M3_talitha_salsabila_data_clean.csv')

    for i,r in df.iterrows():
        doc=r.to_json()
        es.index(index="table_m3_postgres",doc_type="doc",body=doc)

default_args = {
    'owner': 'Talitha',
    'start_date': dt.datetime(2024, 7, 22, 15, 25, 0) - dt.timedelta(hours=7),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
}

with DAG('P2M3_talitha_salsabila_DAG',
         default_args=default_args,
         schedule_interval = '30 6 * * *', 
         ) as dag:

    get_data = PythonOperator(task_id='fetch_data',
                                 python_callable=fetch_data)

    cleanData = PythonOperator(task_id = 'clean_data',
                                 python_callable = clean_data)

    upload_to_ES = PythonOperator(task_id ='load_to_elasticsearch',
                                 python_callable =load_to_elasticsearch)

get_data >>  cleanData >> upload_to_ES