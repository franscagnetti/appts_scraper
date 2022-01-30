# appts_scraper
Appartment scraper Argentina

## TODO:
1. Create clases:
	1.1 for each property -> DONE -> split Floor and Room from address, and maybe split street and number for the address. 
	1.2 for each web scrapper
2. Create docker-compose to start an airflow server and a database.
3. Ingest the data into the database through an airflow DAG.
4. Create ci/cd process.
5. Add more webpages.
6. Paralelize the process (1 thread per page).
7. Create a process to match properties between different web pages and detect which is the best option if there is any.
8. Create an API with auth to return the data required.
9. Migrate all the process to a cloud provider.
10. Small analysis and dashboard.



# Setup environment

## First time:

Execute the following lines
```
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose up airflow-init
```

To start the development environment execute:
```
docker-compose up
```

In other terminal you can look which containers are running executing:
```
docker ps
```

This will initialize the main folders, create the .env file with config parameters and initiate airflow environment and username. Default: user airflow password airflow


## Clean environment

In case you want to revert the changes, you have to run:
```
docker-compose down --volumes --remove-orphans
rm -rf ./dags ./logs ./plugins
```

# DAGs
## Create a DAG
To create a DAG insert it into 'dags' folder

## Test DAG
There are two options to test a DAG:
1. Go to the UI (localhost:8080) and execute it there
2. Search for the docker-container ID and write docker exec <container_id> bash. Then execute DAGs from command line.
