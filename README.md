# appts_scraper
Appartment scraper Argentina

## TODO:
1. Ingest the data into the database through an airflow DAG.
2. Add more webpages.
3. Paralelize the process (1 thread per page).
4. Create a process to match properties between different web pages and detect which is the best option if there is any.
5. Create an API with auth to return the data required.
6. Create ci/cd process.
7. Migrate all the process to a cloud provider.
8. Small analysis and dashboard.



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

# Create user:
docker exec -it containername /bin/bash
airflow users create --username name --firstname name --lastname name --role role --email email
Then type the password

# DAGs
## Create a DAG
To create a DAG insert it into 'dags' folder

## Test DAG
There are two options to test a DAG:
1. Go to the UI (localhost:8080) and execute it there
2. Search for the docker-container ID and write docker exec <container_id> bash. Then execute DAGs from command line.

