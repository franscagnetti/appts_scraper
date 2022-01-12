import requests
import re

from bs4 import BeautifulSoup
from Property import Property

def get_soup(user_agent,site):
    """
        Returns soup object parsed with lxml
    """
    header = {'user-agent':user_agent}
    site_gotten = requests.get(site,headers=header).text
    soup = BeautifulSoup(site_gotten,'lxml')
    return soup

def get_property_list(soup,user_agent):
    """
        Returns a list of properties in json format.
    """
    
    # Looping up to max pages
    max_pages = 1
    counter = 0

    property = {}
    properties_found_list = []

    while True:
        print(f'Looping pages up to number {max_pages+1}')
        print(f'Page : {counter+1}')
        
        prop_list = soup.find_all('div', class_ = 'listing__item')

        for prop in prop_list:
            property_obj = Property()

            # Card details
            card_details = prop.find('div', class_ = 'card__details-box')

            # Card details top
            card_details_top = card_details.find('div', class_ = 'card__details-box-top')

            try:
                card_cost = card_details_top.find('div', class_ = 'card__monetary-values').find('p', class_ = 'card__price').text.strip()
                card_cost = re.findall('\d*\.?\d+',card_cost)[0]
                property_obj.cost = card_cost
            except:
                pass

            try:
                card_currency = card_details_top.find('div', class_ = 'card__monetary-values').find('p', class_ = 'card__price').find('span', class_ = 'card__currency').text.strip()
                property_obj.currency = card_currency
            except:
                pass

            try:
                card_expenses = card_details_top.find('div', class_ = 'card__monetary-values').find('p', class_ = 'card__expenses').text.strip()
                card_expenses_refactored = re.findall("\d+", re.sub('[^A-Za-z0-9]+', '', card_expenses))[0]
                property_obj.expenses = card_expenses_refactored
            except:
                pass

            try:
                main_features = card_details_top.find('div', class_ = 'card__monetary-values').find('ul', class_ = 'card__main-features').find_all('li')
                for feature in main_features:
                    if "icono-superficie_cubierta" in str(feature):
                        property_obj.covered_area = feature.find('span').text.strip()
                    elif "icono-cantidad_dormitorios" in str(feature):
                        property_obj.number_of_rooms = feature.find('span').text.strip()
                    elif "icono-antiguedad" in str(feature):
                        property_obj.antiquity = feature.find('span').text.strip()
                    elif "icono-cantidad_banos" in str(feature):
                        property_obj.number_of_baths = feature.find('span').text.strip()
            except:
                pass

            try:
                card_address = card_details.find('h2', class_ = 'card__address').text.strip()
                property_obj.address = card_address
            except:
                pass

            try:
                card_title_primary = card_details.find('p', class_ = 'card__title--primary').text.strip()
                property['card_title_primary'] = card_title_primary
            except:
                pass

            try:
                card_title = card_details.find('p', class_ = 'card__title').text.strip()
                property['card_title'] = card_title
            except:
                pass

            try:
                card_info = card_details.find('p', class_ = 'card__info ').text.strip()
                property['card_info'] = card_info
            except:
                pass

            # Append JSON
            properties_found_list.append(property_obj)
        

        # Find next page
        next_page = soup.find_all('li', class_ = 'pagination__page-next')

        try:
            print('next_Page')
            url_slug = next_page[0].find('a',rel='next',href=True)
            if url_slug:
                url = f'https://www.argenprop.com{url_slug["href"]}'
                print(f'Next page is: {url}')
                soup = get_soup(user_agent,url)
            else:
                print("No next page")
                break
        except Exception as inst:
            print(f"Error : {inst}")
            break
        
        if counter == max_pages:
            print(f'Automatically stopping page iteration at : {counter}')
            break
        else:
            counter = counter + 1

    return properties_found_list

