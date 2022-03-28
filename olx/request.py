import re
import locale
from datetime import date, datetime, timedelta

import requests
from domain.model import Offer
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL, 'pl_PL')

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
        search = search
        search = f'q-{search}'
    if not category:
        category = 'oferty'
    main_parts = [category, subcategory, subsubcategory, localization, search, data_part]
    for part in main_parts:
        if part:
            part = f'{part}/'
            url += part
    else:
        url = url.rstrip('&/')
    url = base + url
    return url

def get_price_from_string(text):
    if 'darmo' in text:
        return 0
    text = text.replace(' ', '').replace(',', '.')
    pattern = re.compile('[0-9]+(.[0-9]+)?')
    try:
        price = float(pattern.search(text)[0])
    except:
        return -1
    return price

def get_date_from_olx_string(text):
    '''Funtion is creating a datetime variable from string from olx site'''
    # TODO olx string doesnt't care about year and always shows month and day for each offer.
    # The wrong date would be assigned in January if the offer was placed in december,
    # new year instead last year
    def time_to_numbers(text):
        re_time = re.compile(r'(\d\d):(\d\d)')
        hours, minutes = re_time.search(text).groups()
        hours = int(hours)
        minutes = int(minutes)
        return hours, minutes
        
    out = None
    if 'dzisiaj' in text:
        tmp_date = date.today()
        hours, minutes = time_to_numbers(text)
        out = datetime(tmp_date.year, tmp_date.month, tmp_date.day, hours, minutes)
    elif 'wczoraj' in text:
        tmp_date = date.today() - timedelta (days = 1)
        hours, minutes = time_to_numbers(text)
        out = datetime(tmp_date.year, tmp_date.month, tmp_date.day, hours, minutes)
    else:
        try:
            out = datetime.strptime(text, "%d %b")
            out = out.replace(year=date.today().year)
        except ValueError as e:
            print(str(e))
    return out
    


class OlxHandler():

    def __init__(self, search = '', category = '', subcategory = '', subsubcategory = '', localization = '', act_page = None):
        self.search = search
        self.category = category
        self.subcategory = subcategory
        self.subsubcategory = subsubcategory
        self.localization = localization

        self.max_page = 0
        self.act_page = act_page
        self.data = dict()
        self.offers = []
        self.soup = None
        self.errors = []

        #self.update_url()
        self.get_soup()
        self._get_offers_from_olx_soup()

    def __repr__(self) -> str:
        return f"OlxHandler('{self.search}', '{self.category}', '{self.subcategory}', act_page = {self.act_page})"

    @property
    def url(self):
        self._url = build_olx_url(self.search, self.category, self.subcategory, self.subsubcategory, self.localization, self.data, self.act_page)
        return self._url
    
    def get_soup(self):
        #self.update_url()
        r = requests.get(self.url)
        try:
            soup = BeautifulSoup(r.content, 'html.parser')
        except:
            print(f'Problem z uzyskaniem danych strony, {r.status_code}')
            return -1
        self.soup = soup
        return soup

    def get_offers(self):
        self.get_soup()
        table_soup = self._get_offers_from_olx_soup()
        for offer_soup in table_soup:
            offer_data = self._get_data_from_olx_offer(offer_soup)
            offer = Offer(**offer_data)
            self.offers.append(offer)

    def clear_offers(self):
        self.offers.clear()

    def _get_offers_from_olx_soup(self):
        try:   
            offer_table = self.soup.find('table',{'summary':'Ogłoszenia'}).find_all('tr', {'class':'wrap'})
            self.max_page = int(self.soup.find('a', {'data-cy':'page-link-last'}).text.strip())
            print("Znaleziono {} ofert na stronie: {}".format((len(offer_table)), self.url))
        except Exception as e:
            error_msg = f'Niespodziewana zawartość strony: {str(e)}'
            print(error_msg)
            self.errors.append(error_msg)
            return -1
        return offer_table



    def _get_data_from_olx_offer(self, offer):    
        date = offer.find('i', {'data-icon':'clock'}).parent.text
        date = get_date_from_olx_string(date)
        title = offer.strong.text
        try:
            price = offer.find('p', {'class':'price'}).text.strip()
            price = get_price_from_string(price)
        except:
            price = -1

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

    def save_soup_to_file(self):
        with open("data/soup.html", mode='w', encoding = self.soup.original_encoding) as f:
            f.write(str(self.soup))

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
        search = search
        search = f'q-{search}'
    if not category:
        category = 'oferty'
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
    r = requests.get(url, timeout = 2.5)
    try:
        soup = BeautifulSoup(r.content, 'html.parser')
    except:
        print(f'Problem z uzyskaniem danych strony, {r.status_code}')
        return -1
    return soup

def get_offers_from_olx_soup(soup):
    try:   
        offer_table = soup.find('table',{'summary':'Ogłoszenia'}).find_all('tr', {'class':'wrap'})
        max_page = int(soup.find('a', {'data-cy':'page-link-last'}).text.strip())
        print("Znaleziono {} ofert".format(len(offer_table)))
    except:
        print('Niespodziewana zawartość strony')
        return -1
    return offer_table



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

