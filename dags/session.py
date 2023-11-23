from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from db import POSTGRES_NAME
from db import POSTGRES_HOST
from db import POSTGRES_PORT
from db import POSTGRES_USER
from db import POSTGRES_PASSWORD
from db import POSTGRES_SCHEMA

Base = declarative_base()
connection_url = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'
engine = create_engine(
    f'{connection_url}?client_encoding=utf8',
    echo=True,
)
Session = sessionmaker(bind=engine)
