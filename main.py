# pip3 install beautifulsoup4
# pip3 install lxml

from requests.api import head
import pandas as pd
from classes.ScraperInterface import ArgenpropScraper

if __name__ == "__main__":
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
    print(df.head())
    df.to_csv('property_list.csv', index=False, encoding='utf-8')