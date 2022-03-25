import os

from olx.request import *
from domain.model import Offer

def main():

    data = {
        'filter_float_price:from':10,
        'filter_float_price:to':100,
        'courier':1,
    }

    url = build_olx_url(
        search = 'pióro', 
        category='sport-hobby', 
        subcategory='kolekcje', 
        data = data,
        ) 
    soup = get_olx_soup(url)
    table = get_offers_from_olx_soup(soup)



if __name__ == '__main__':          
    main()

