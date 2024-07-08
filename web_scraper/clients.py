import os
from sqlalchemy import engine, create_engine

def get_mysql_traveldata_conn() -> engine.base.Connection:
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")

    address = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(address)
    connect = engine.connect()
    return connect
