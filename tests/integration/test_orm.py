from domain import model
from datetime import datetime

def test_offer_mapper_can_load_lines(session):
    session.execute(
        "INSERT INTO offers (title, price, delivery, date) VALUES "
        "('Monitor', 45.30, true, '2011-04-11 00:00:00'),"
        "('Klucz', 45.30, true, '2011-04-11 00:00:00')"

    )
    expected = [
        model.Offer("Monitor", 45.30, True, datetime(2011, 4, 11)),
        model.Offer("Klucz", 45.30, True, datetime(2011, 4, 11)),
    ]
    assert True
    assert session.query(model.Offer).all() == expected