from datetime import date
import re

import requests
import urllib.parse
from bs4 import BeautifulSoup


url = 'https://www.olx.pl/sport-hobby/rowery/krakow/?search%5Bfilter_float_price%3Afrom%5D=20'

def encode_url():
    pass

def decode_url():
    pass

def build_olx_url(search = '', category = '', subcategory = '', subsubcategory = '', localization = '', data = None, page = None):
    '''Function for building olx adress with selected categiries, filters and other settings'''

    '''
    EXAMPLES
    https://www.olx.pl/sport-hobby/rowery/bmx/?search%5Bfilter_float_price%3Afrom%5D=20&search%5Bfilter_float_price%3Ato%5D=50&search%5Bfilter_enum_state%5D%5B0%5D=used&search%5Bphotos%5D=1&search%5Bdescription%5D=1
    https://www.olx.pl/sport-hobby/rowery/bmx/?search[filter_float_price:from]=20&search[filter_float_price:to]=50&search[filter_enum_state][0]=used&search[photos]=1&search[description]=1
    data filers: 
    filter_float_price:from
    filter_float_price:to
    description
    courier
    https://www.olx.pl/krakow/q-pi%C5%82ka/?search%5Bfilter_float_price%3Afrom%5D=10&search%5Bfilter_float_price%3Ato%5D=100&page=2
    '''
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

def print_offers(url, n = 10):
    r = requests.get(url)
    try:
        soup = BeautifulSoup(r.content, 'html.parser')
    except:
        print(f'Problem z uzyskaniem danych strony, {r.status_code}')
        return -1
    try:   
        offer_table = soup.find('table',{'summary':'Ogłoszenia'}).find_all('tr', {'class':'wrap'})
        print("Znaleziono {} ofert".format(len(offer_table)))
    except:
        print('Niespodziewana zawartość strony')
        return -1
     
    for offer in offer_table[0:n]:
        date = offer.find('i', {'data-icon':'clock'}).parent.text
        name = offer.strong.text
        price = offer.find('p', {'class':'price'}).text.strip()
        if offer.find('div', {'class':'olx-delivery-icon'}):
            delivery = True
        else:
            delivery = False

        print(f'{date:12}\t{price:10}{delivery}\t{name}')
       
data = {
    'filter_float_price:from':10,
    'filter_float_price:to':100,
    'courier':1,
}

#Debug
url = build_olx_url(search = 'piłka', category = '', subcategory = '', subsubcategory = '', localization = 'krakow', data = data, page = 2232)
print(url)
print_offers(url)

