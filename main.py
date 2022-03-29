import os

from olx.request import *
from domain.model import Offer

def main():

    h = OlxHandler('monitor dell')
    h.get_offers()
    h.get_more_offers(break_on_same=True, to_page=5)

    print(h.offers[-1])
    return
    
if __name__ == '__main__':          
    main()

