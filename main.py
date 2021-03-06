import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from olx.request import *
from domain.model import Offer
from adapters import orm
from adapters.orm import metadata
from adapters.session import get_session

def get_session__():
    engine = create_engine(config.get_postgres_uri())
    metadata.create_all(engine)
    orm.start_mappers()
    get_session = sessionmaker(bind=engine)
    return get_session()

def main():
    session = get_session()

    h = OlxHandler('monitor dell')
    h.get_offers()
    h.get_more_offers(to_page=3)

    print(h.offers[-1])
    o1 = h.offers[-1]

    for i in h.offers:
        session.add(i)
    session.commit()

    return

if __name__ == '__main__':          
    main()

