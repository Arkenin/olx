import pytest
import requests
from olx.request import *

from datetime import datetime

def test_olx_handler():
    h = OlxHandler()
    h.get_offers()
    assert len(h.offers) > 0

def test_build_olx_url():   
    data = {
        'filter_float_price:from':10,
        'filter_float_price:to':100,
        'courier':1,
    }
    assert build_olx_url() == 'https://www.olx.pl/oferty'
    assert build_olx_url(search = 'pióro') == 'https://www.olx.pl/oferty/q-pióro'
    url = build_olx_url(
        search = 'pióro', 
        category='sport-hobby', 
        subcategory='kolekcje', 
        data = data,
        ) 
    assert url == 'https://www.olx.pl/sport-hobby/kolekcje/q-pióro/?search[filter_float_price:from]=10&search[filter_float_price:to]=100&search[courier]=1'

def test_olx_soup():
    url = 'https://www.olx.pl/oferty/q-pióro'
    soup = get_olx_soup(url)
    assert bool(get_offers_from_olx_soup(soup))

def test_get_date_from_olx_string():
    current_year = datetime.today().year
    today = date.today()
    yesterday = date.today() - timedelta (days = 1)
    assert get_date_from_olx_string("23 mar") == datetime(day = 23, month = 3, year = current_year)
    assert get_date_from_olx_string("23 lut") == datetime(day = 23, month = 2, year = current_year)
    assert get_date_from_olx_string("wczoraj o 01:23") == datetime(day = yesterday.day,
                                                                     month = yesterday.month,
                                                                     year = yesterday.year,
                                                                     hour=1,
                                                                     minute=23)
    assert get_date_from_olx_string("dzisiaj o 23:45") == datetime(day = today.day,
                                                                     month = today.month,
                                                                     year = today.year,
                                                                     hour=23,
                                                                     minute=45)
    assert get_date_from_olx_string("nothing") == None

def test_get_price_from_string():
    assert get_price_from_string(":125zł") == 125
    assert get_price_from_string("25.2  zł") == 25.2
    assert get_price_from_string("Za darmo") == 0
    assert get_price_from_string("ksngd3") == 3
    assert get_price_from_string("15 000ZŁ") == 15000
    assert get_price_from_string("35,3") == 35.3
    assert get_price_from_string("") == None
    assert get_price_from_string("nic") == None
