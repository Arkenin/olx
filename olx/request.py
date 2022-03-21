from datetime import date
import re

import requests
from bs4 import BeautifulSoup

url = 'https://www.olx.pl/sport-hobby/rowery/krakow/?search%5Bfilter_float_price%3Afrom%5D=20'

def build_olx_url():
    category = ''
    filters = {}
    localization = ''
    dist_from_loc = 0
    photo = None        # True, False or None
    delivery = None     # True, False or None
    pass

def print_offers(url, n = 10):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        offer_table = soup.find('table',{'summary':'Ogłoszenia'}).find_all('tr', {'class':'wrap'})
        print("Znaleziono {} ofert".format(len(offer_table)))

        for offer in offer_table[0:n]:
            date = offer.find('i', {'data-icon':'clock'}).parent.text
            name = offer.strong.text
            price = offer.find('p', {'class':'price'}).text.strip()
            if offer.find('div', {'class':'olx-delivery-icon'}):
                delivery = True
            else:
                delivery = False

            print(f'{date:12}\t{price:10}{delivery}\t{name}')
        
    except:
        print('ERROR')

    pass

print_offers(url)

