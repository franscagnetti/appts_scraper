from bs4 import BeautifulSoup
import requests
import re
from abc import ABC, abstractmethod
from .Property import Property

class ScraperInterface(ABC):
    
    def __init__(self, user_agent: str, site: str):
        #super().__init__()
        user_agent = user_agent
        base_site = site
    
    def get_soup(self,  site: str):
        """
          set object's soup
        """
        header = {'user-agent':self.user_agent}
        site_gotten = requests.get(site,headers=header).text
        return BeautifulSoup(site_gotten,'lxml')

    @abstractmethod
    def get_property_list(self, soup, user_agent: str) -> List[Property]:
    """
        Returns a list of properties in json format.
    """
    pass