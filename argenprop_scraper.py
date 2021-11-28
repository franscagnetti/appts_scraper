#!/usr/bin/env python
# coding: utf-8

# In[106]:


from bs4 import BeautifulSoup
import requests
import re


# In[113]:


def get_soup(user_agent,site):
    """
        devuelve objeto soup para la url del argumento, parseada con lxml
    """
    header = {'user-agent':user_agent}
    site_gotten = requests.get(site,headers=header).text
    soup = BeautifulSoup(site_gotten,'lxml')
    return soup


# In[140]:


def get_apartment_list(soup_list,price):
    """
        Devuelve lista de departamentos -en soup_list- si son menores al precio que viene como argumento.
        TODO -> filtrar o generar tipo de cambio si es USD
        TODO -> cambiar a diccionario para agregar precio
        TODO -> pensar si agregar más filtros
    """
    apartment_list = []
    for item in soup_list:
        try:
            precio_class = re.findall(r'\d+',item.find('p',class_='card__price').text)
            precio = ''.join(precio_class)
        except:
            precio = '50000000'
        try:
            expensas_class = re.findall(r'\d+',item.find('p',class_='card__expenses').text)
            expensas = '0' if expensas_class is None else ''.join(expensas_class)
        except:
            expensas = '0'
        if(precio):
            if(int(precio) + int(expensas) < price):
                for a in item.find_all('a',href=True):
                    if('Descartados' not in a['href']):
                        apartment_list.append(f'https://www.argenprop.com{a["href"]}')
                        
    return apartment_list


# In[141]:


if __name__ == "__main__":
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34'
    site = 'https://www.argenprop.com/departamento-alquiler-barrio-belgrano'
    belgrano_soup = get_soup(user_agent,site)
    belgrano_items = belgrano_soup.find_all('div',class_='listing__item')
    lista_depas = get_apartment_list(belgrano_items,80000)
    for item in lista_depas:
        print(item)


# In[ ]:




