# pip3 install beautifulsoup4
# pip3 install lxml

from requests.api import head
import argenprop_scraper as aps
import csv
import pandas as pd

if __name__ == "__main__":
    #set soup
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    site = 'https://www.argenprop.com/inmuebles-pais-argentina'

    soup = aps.get_soup(user_agent,site)
    property_list = aps.get_property_list(soup)

    # Write data into csv
    df = pd.DataFrame.from_records(property_list)
    print(df.head())
    df.to_csv('property_list.csv', index=False, encoding='utf-8')