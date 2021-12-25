from bs4 import BeautifulSoup
import requests
import re


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
        Devuelve lista de departamentos -en soup_list- si son menores al precio que viene como argumento.
        TODO -> filtrar o generar tipo de cambio si es USD
        TODO -> cambiar a diccionario para agregar precio
        TODO -> pensar si agregar más filtros
    """


    property_list = []

    # TODO: first we work with 1 appt, after we define it we can move to a for iteration for all the appartments
    # TODO: add more variables to the appartment
    property = {}

    appt = soup.find('div', class_ = 'listing__item')
    card_details = appt.find('div', class_ = 'card__details-box')
    card_details_top = card_details.find('div', class_ = 'card__details-box-top')

    card_cost = card_details_top.find('div', class_ = 'card__monetary-values').find('p', class_ = 'card__price').text.strip()
    card_cost = re.findall('\d*\.?\d+',card_cost)[0]

    card_currency = card_details_top.find('div', class_ = 'card__monetary-values').find('p', class_ = 'card__price').find('span', class_ = 'card__currency').text.strip()

    property['card_cost'] = card_cost
    property['card_currency'] = card_currency
    property_list.append(property)

    return property_list

    # for item in soup_list:
    #     appartment = {}
    #     try:
    #         precio_class = re.findall(r'\d+',item.find('p',class_='card__price').text)
    #         precio = ''.join(precio_class)
    #     except:
    #         precio = '50000000'
    #     try:
    #         expensas_class = re.findall(r'\d+',item.find('p',class_='card__expenses').text)
    #         expensas = '0' if expensas_class is None else ''.join(expensas_class)
    #     except:
    #         expensas = '0'
    #     if(precio):
    #         if(int(precio) + int(expensas) < price):
                # for a in item.find_all('a',href=True):
                #     if('Descartados' not in a['href']):
                #         property_list.append(f'https://www.argenprop.com{a["href"]}')