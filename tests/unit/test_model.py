import pytest
from domain.model import Offer

from datetime import datetime
def test_offer_creating():
    Offer("Produkt")
    Offer("Produkt", 20, False)
    with pytest.raises(TypeError) as e_info:
        Offer("Produkt", 2, 20)
    
    with pytest.raises(ValueError) as e_info:
        Offer("Produkt", -3, False)

    


def test_offer_equality():
    assert Offer('Protukt 1', price = 12) == Offer('Protukt 1', price = 12)
    assert Offer('Other 1', price = 12) != Offer('Protukt 1', price = 12)
    assert Offer('Protukt 1', price = 5) != Offer('Protukt 1', price = 12)

    assert Offer('Protukt 1', delivery= True, price = 12) == Offer('Protukt 1', price = 12)
    

    f1 = Offer('Protukt 1', price = 12, date = datetime(2022,10,10))
    f11 = Offer('Protukt 1', price = 12, date = datetime(2021,10,10))
    f2 = Offer('Protukt 2', price = 12, date = datetime(2022,10,10))
    f22 = Offer('Protukt 2', price = 10, date = datetime(2022,10,10))

    assert f1 == f11
    assert f1 != f2
    assert f1 == f11
    
def test_offer_in_list():
    batch = [
    Offer('Protukt 1', price = 12, date = datetime(2022,10,10)),
    Offer('Protukt 2', price = 12, date = datetime(2022,10,10)),
    Offer('Protukt 2', price = 10, date = datetime(2022,10,10)),
    ]

    one = Offer('Protukt 1', price = 12, date = datetime(2021,10,10))
    two = Offer('Rare Item', price = 12, date = datetime(2021,10,10))
    assert one in batch
    assert two not in batch