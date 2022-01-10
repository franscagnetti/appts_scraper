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