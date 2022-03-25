import pytest
import requests
from olx.request import build_olx_url, get_olx_soup, get_offers_from_olx_soup, get_price_from_string

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

def test_get_price_from_string():
    assert get_price_from_string(":125zł") == 125
    assert get_price_from_string("25.2  zł") == 25.2
    assert get_price_from_string("Za darmo") == 0
    assert get_price_from_string("ksngd3") == 3
    assert get_price_from_string("35,3") == -1
    assert get_price_from_string("") == -1
    assert get_price_from_string("nic") == -1
    assert get_price_from_string("5,566,566.5") == -1
