import sqlite3
import json
from pathlib import Path
import re
import pandas as pd
import numpy as np
import time

# products = 

from bs4 import BeautifulSoup
import requests
from lxml import etree
  
# Website URL
main_url = 'https://www.zoopla.co.uk/'
  
# class list set
class_list = set()

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})


# URL = 'https://www.zoopla.co.uk/for-sale/property/manchester/?q=manchester&search_source=home'

cities = ['sheffield']
# ['manchester', 'aberdeenshire', 'birmingham', 'bristol', 'edinburgh', 'glasgow', 'liverpool', 'london', 'nottingham', 'buckinghamshire', 'gloucestershire', 'oxford', 'hampshire', 'sheffield']
main_add = []

for city in cities:
    URL = f'https://www.zoopla.co.uk/for-sale/property/{city}/?q={city}&search_source=home'
    print(city)

    for i in range(200):
        # print(i)
        # Page content from Website URL

        URL = f'https://www.zoopla.co.uk/for-sale/property/{city}/?q={city}&search_source=home&pn={i}'
        try:
            page = requests.get( URL, headers=HEADERS )
        except:
            break

        # parse html content
        soup = BeautifulSoup( page.content , 'html.parser')

        # dom = etree.HTML(str(soup))
        
        # class changes everyday, find the class of the element which contains link to that house
        x1 = [i['href'] for i in soup.find_all('a', {'class': 'ee6kn4s10 css-1gdcbd8-StyledLink-Link e33dvwd0'})]
        #                                                      ee6kn4s10 css-1gdcbd8-StyledLink-Link e33dvwd0
         

        regex = r'/(.*)/.*'

        x1 = [main_url + re.search(regex, x).group(1) for x in x1]
        # print(x1)

        for k in x1:
            main_add.append([k, city])

        # time.sleep(2)
        # try:
        #     next = soup.find('a', string='Next >')['href']
        # except:
        #     break

        # URl = main_url + next


address_df = pd.DataFrame(np.array(main_add))
address_df.columns = ['houses', 'city']
address_df.to_csv('main_house_links.csv')
# address_df.to_csv('manchester.csv')