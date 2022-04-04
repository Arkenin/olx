import os

def get_postgres_uri():
    dev_host = '132.226.203.134'
    host = os.environ.get('DB_HOST', dev_host)
    port = 7900 if host == dev_host else 5432
    password = os.environ.get('DB_PASSWORD', 'abc123')
    user, db_name = 'olx', 'olx'
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"