from sqlalchemy import (
    Table, MetaData, Column, Integer, String, DateTime,
    Boolean, Float, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from domain import model

metadata = MetaData()

offers = Table(
    'offers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('price', Float, nullable=False),
    Column('delivery', Boolean()),
    Column('date', DateTime()),
)

def start_mappers():
    offers_mapper = mapper(model.Offer, offers, properties={
    '_title': offers.c.title,
    '_price': offers.c.price,
    '_delivery': offers.c.delivery,
    })

