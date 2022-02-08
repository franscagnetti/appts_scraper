from datetime import datetime
from airflow import DAG
from requests.api import head
import pandas as pd
from airflow.operators.python_operator import PythonOperator
from classes.argenpropScraper import ArgenpropScraper
import os

cwd = os.getcwd()

def execute():
    #set soup
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    site = 'https://www.argenprop.com/inmuebles-pais-argentina'

    argScraper = ArgenpropScraper()
    
    soup = argScraper.get_soup(user_agent,site)
    property_list = argScraper.get_property_list(soup, user_agent)

    prop_list_to_dict = []
    [prop_list_to_dict.append(ob.__dict__) for ob in property_list]

    # Write data into csv
    df = pd.DataFrame.from_records(prop_list_to_dict)
    print(f'Creating csv at: {cwd}/property_list.csv')
    df.to_csv('property_list.csv', index=False, encoding='utf-8')

dag = DAG('sample_dag', description='Hello World DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2017, 3, 20), catchup=False)

hello_operator = PythonOperator(task_id='hello_task', python_callable=execute, dag=dag)

hello_operator