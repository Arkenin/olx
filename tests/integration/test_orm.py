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
    assert session.query(model.Offer).all() == expected

def test_offer_mapper_can_save(session):
    nice_offer = model.Offer("RTX3060", 250, True, datetime(2022, 4, 11))
    session.add(nice_offer)
    session.commit()

    rows = list(session.execute('SELECT title, price, delivery, date FROM "offers"'))
    assert rows == [('RTX3060', 250.0, 1, '2022-04-11 00:00:00.000000')]

def test_saving_offer_object(session):
    nice_offer = model.Offer("RTX3060", 250, True, datetime(2022, 4, 11))
    session.add(nice_offer)
    session.commit()
    test_object = session.query(model.Offer).filter_by(id=1).one()

    assert test_object.title == 'RTX3060'
    assert test_object.price == 250
    assert test_object.delivery == True
    assert test_object.date == datetime(2022, 4, 11, 0, 0)

