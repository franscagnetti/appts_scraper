# pip3 install beautifulsoup4
# pip3 install lxml

from bs4 import BeautifulSoup
import requests
from requests.api import head
import re
import argenprop_scraper as aps


# TODO: add class_ listing__item listing__item--featured

# appt = soup.find('div', class_ = 'listing__item')
# card_details = appt.find('div', class_ = 'card__details-box')
# card_details_top = card_details.find('div', class_ = 'card__details-box-top')

# card_cost = card_details_top.find('div', class_ = 'card__monetary-values').find('p', class_ = 'card__price').text.strip()
# card_cost = re.findall('\d*\.?\d+',card_cost)[0]

# card_currency = card_details_top.find('div', class_ = 'card__monetary-values').find('p', class_ = 'card__price').find('span', class_ = 'card__currency').text.strip()

# print(card_currency)
# print(card_cost)

if __name__ == "__main__":
    #set soup
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    site = 'https://www.argenprop.com/inmuebles-pais-argentina'

    soup = aps.get_soup(user_agent,site)

    appts_list = aps.get_apartment_list(soup)

    print("Returning all the appartments found")
    for item in appts_list:
        print(item)