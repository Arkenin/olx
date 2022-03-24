import pytest
import os

print('--------------')
print(os.getcwd())

import requests
from olx.request import build_olx_url


data = {
    'filter_float_price:from':10,
    'filter_float_price:to':100,
    'courier':1,
}

def test_build_olx_url():   
    assert build_olx_url() == 'https://www.olx.pl/'
    assert build_olx_url(search = 'pióro') == 'https://www.olx.pl/oferty/q-pi%C3%B3ro/'
    assert build_olx_url() == 'https://www.olx.pl/'


