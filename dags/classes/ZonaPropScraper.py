from .ScraperInterface import ScraperInterface
from .Property import Property
import re
from bs4 import BeautifulSoup

class ZonaPropScraper(ScraperInterface):
    def get_property_list(self) -> List[Property]:
        """
            Returns a list of properties in json format.
        """
        
        # Looping up to max pages
        max_pages = 1
        counter = 0
        
        # Initial soup
        soup = super().get_soup(self.base_site)
        
        property = {}
        properties_found_list = []

        while True:
            print(f'Looping pages up to number {max_pages+1}')
            print(f'Page : {counter+1}')
            
            prop_list = soup.find_all('div', class_ = 'postingCardContent')

            for prop in prop_list:
                property_obj = Property()

                # property price and location
                card_price_location_details = prop.find('div', class_ = 'postingCardRowPriceLocation')

                # property rooms and size
                card_rooms_details = prop.find('div', class_ = 'postingCardMainFeaturesBlock')

                try:
                    card_cost = card_price_location_details.find('div', class_ = 'postingCardPrices').find('span', class_ = 'firstPrice').text.strip()
                    card_cost_clean = re.findall('\d*\.?\d+',card_cost)[0]
                    property_obj.cost = card_cost
                except:
                    pass

                try:
                    card_currency = card_price_location_details.find('div', class_ = 'postingCardPrices').find('span', class_ = 'firstPrice').text.strip()
                    card_currency_clean = re.findall('^[^0-9| ]*',card_currency)[0]
                    property_obj.currency = card_currency_clean
                except:
                    pass

                try:
                    #should add expenses currency?
                    card_expenses = card_price_location_details.find('div', class_ = 'postingCardPrices').find('span', class_ = 'postingCardExpenses').text.strip()
                    card_expenses_clean = re.findall('[0-9]*', card_expenses)[0]
                    property_obj.expenses = card_expenses_refactored
                except:
                    pass
                
                 try:
                    card_address = card_price_location_details.find('div', class_ = 'postingCardLocationBlock').find('span',class_' postingCardLocationTitle').text.strip()
                    property_obj.address = card_address
                except:
                    pass
                
                try:
                    card_location = card_price_location_details.find('div', class_ = 'postingCardLocationBlock').find('span',class_' postingCardLocation').find('span',_class=None).text.strip() ## test here
                    ## TODO check if it's necessary to split city and province
                    property_obj.city = card_location
                except:
                    pass
                
                ## TODO test. 
                ## Add card_rooms_details and next page logic
                break

        return properties_found_list