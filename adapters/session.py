import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

import config
from adapters import orm
from adapters.orm import metadata

def get_session():
    engine = create_engine(config.get_postgres_uri())
    if check_database(engine):
        metadata.create_all(engine)
        orm.start_mappers()
        get_session = sessionmaker(bind=engine)
        return get_session()

def check_database(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            engine.connect()
            return True
        except OperationalError:
            time.sleep(0.5)
    print('Baza Postgres się nie uruchomiła')
    return False