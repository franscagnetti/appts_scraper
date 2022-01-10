from bs4 import BeautifulSoup
import requests
import re

class Property:
    def __init__(self, address = 'undefined', floor = 0, room = 'A', city = 'undefined', cost = 0, expenses = 0, currency = 'undefined', number_of_rooms = 0, number_of_baths = 0, covered_area = 0):
        self.address = address
        self.floor = floor
        self.room = room
        self.city = city
        self.cost = cost
        self.expenses = expenses
        self.currency = currency 
        self.number_of_rooms = number_of_rooms
        self.number_of_baths = number_of_baths
        self.covered_area = covered_area

def get_soup(user_agent,site):
    """
        Returns soup object parsed with lxml
    """
    header = {'user-agent':user_agent}
    site_gotten = requests.get(site,headers=header).text
    soup = BeautifulSoup(site_gotten,'lxml')
    return soup

def get_property_list(soup):
    """
        Returns a list of properties in json format.
        TODO -> filtrar o generar tipo de cambio si es USD
        TODO -> cambiar a diccionario para agregar precio
        TODO -> pensar si agregar más filtros
    """

    
    property_list = []

    # TODO: first we work with 1 props, after we define it we can move to a for iteration for all the appartments
    # TODO: add more variables to the appartment
    
    max_pages = 3
    counter = 0
    while True:
        print('Looping pages')
        
        prop_list = soup.find_all('div', class_ = 'listing__item')
        for prop in prop_list:
            property = {}
            # Card details
            card_details = prop.find('div', class_ = 'card__details-box')

            # Card details top
            card_details_top = card_details.find('div', class_ = 'card__details-box-top')

            try:
                card_cost = card_details_top.find('div', class_ = 'card__monetary-values').find('p', class_ = 'card__price').text.strip()
                card_cost = re.findall('\d*\.?\d+',card_cost)[0]
                property['card_cost'] = card_cost
            except:
                pass

            try:
                card_currency = card_details_top.find('div', class_ = 'card__monetary-values').find('p', class_ = 'card__price').find('span', class_ = 'card__currency').text.strip()
                property['card_currency'] = card_currency
            except:
                pass

            try:
                card_expenses = card_details_top.find('div', class_ = 'card__monetary-values').find('p', class_ = 'card__expenses').text.strip()
                card_expenses_refactored = re.findall("\d+", re.sub('[^A-Za-z0-9]+', '', card_expenses))[0]

                property['card_expenses'] = card_expenses_refactored
                property['card_expenses_currency'] = 'ARS'
            except:
                pass

            try:
                main_features = card_details_top.find('div', class_ = 'card__monetary-values').find('ul', class_ = 'card__main-features').find_all('li')
                for feature in main_features:
                    if "icono-superficie_cubierta" in str(feature):
                        property['covered_area'] = feature.find('span').text.strip()
                    elif "icono-cantidad_dormitorios" in str(feature):
                        property['number_of_rooms'] = feature.find('span').text.strip()
                    elif "icono-antiguedad" in str(feature):
                        property['antiquity'] = feature.find('span').text.strip()
                    elif "icono-cantidad_banos" in str(feature):
                        property['number_of_baths'] = feature.find('span').text.strip()
            except:
                pass

            try:
                card_address = card_details.find('h2', class_ = 'card__address').text.strip()
                property['card_address'] = card_address
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
            property_list.append(property)
        
        next_page = soup.find_all('li', class_ = 'pagination__page-next')
        
        #Next Page
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
            print(f'Automatically topping page iteration at : {counter}')
            break
        else:
            counter = counter + 1

    return property_list

def get_property_list_obj(soup,user_agent):
    """
        Returns a list of properties in json format.
        TODO -> filtrar o generar tipo de cambio si es USD
    """
    
    # Looping up to max pages
    max_pages = 1
    counter = 0
    properties_found_list = []
    while True:
        print(f'Looping pages up to number {max_pages+1}')
        print(f'Page : {counter+1}')
        
        prop_list = soup.find_all('div', class_ = 'listing__item')
        for prop in prop_list:
            property = {}
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
                        property['antiquity'] = feature.find('span').text.strip()
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
            property_list.append(property)
            properties_found_list.append(property_obj)
        
        next_page = soup.find_all('li', class_ = 'pagination__page-next')
        
        #Next Page
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

