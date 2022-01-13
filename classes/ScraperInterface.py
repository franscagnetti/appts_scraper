from bs4 import BeautifulSoup
import requests
import re
from abc import ABC, abstractmethod
from .Property import Property

class ScraperInterface(ABC):

  def __init__(self):
        super().__init__()

  def get_soup(self, user_agent: str, site: str):
      """
          Returns soup object parsed with lxml
      """
      header = {'user-agent':user_agent}
      site_gotten = requests.get(site,headers=header).text
      soup = BeautifulSoup(site_gotten,'lxml')
      return soup

  @abstractmethod
  def get_property_list(self, soup, user_agent: str):
    """
        Returns a list of properties in json format.
    """
    pass