from datetime import date
import re

import requests
from bs4 import BeautifulSoup


url = 'https://www.olx.pl/sport-hobby/rowery/krakow/?search%5Bfilter_float_price%3Afrom%5D=20'

def encode_url():
    pass

def decode_url():
    pass

def build_olx_url(search = '', category = '', subcategory = '', subsubcategory = '', localization = '', data = None, page = None):
    '''Function for building olx adress with selected categiries, filters and other settings'''

    base = 'https://www.olx.pl/'
    url = ''
    data_part = ''
    if data or page:
        data_part = '?'
        for key, value in data.items():
            data_part += f'search[{key}]={value}&'
            #data_part += requests.utils.quote(f'search[{key}]') + f"={value}&"
        if page:
            data_part += f'page={page}'
    if search:
        search = requests.utils.quote(search)
        search = f'q-{search}'
    main_parts = [category, subcategory, subsubcategory, localization, search, data_part]
    for part in main_parts:
        if part:
            part = f'{part}/'
            url += part
    else:
        url = url.rstrip('&/')
    url = base + url
    return url 

def get_olx_soup(url):
    r = requests.get(url)
    try:
        soup = BeautifulSoup(r.content, 'html.parser')
    except:
        print(f'Problem z uzyskaniem danych strony, {r.status_code}')
        return -1
    return soup

def get_offers_from_olx_soup(soup):
    try:   
        offer_table = soup.find('table',{'summary':'Ogłoszenia'}).find_all('tr', {'class':'wrap'})
        print("Znaleziono {} ofert".format(len(offer_table)))
    except:
        print('Niespodziewana zawartość strony')
        return -1
    return offer_table

def get_price_from_string(text):
    pattern = re.compile('[0-9]+(.[0-9]+)?')
    return float(pattern.search(text)[0])

def get_data_from_olx_offer(offer):    
    date = offer.find('i', {'data-icon':'clock'}).parent.text
    title = offer.strong.text
    price = offer.find('p', {'class':'price'}).text.strip()
    price = get_price_from_string(price)
    if offer.find('div', {'class':'olx-delivery-icon'}):
        delivery = True
    else:
        delivery = False
    data = {
        'date':date,
        'title':title,
        'price':price,
        'delivery':delivery,
    }
    return data



data = {
    'filter_float_price:from':10,
    'filter_float_price:to':100,
    'courier':1,
}

# #Debug
# url = build_olx_url(search = 'piłka', category = '', subcategory = '', subsubcategory = '', localization = 'krakow', data = data, page = 2232)
# print(url)
# print_offers(url)

