from sqlalchemy import Integer, String, Column, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

from session import Base

class Webinar(Base):
    __tablename__ = 'webinar'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    webinar_date = Column(DateTime, nullable=False, default=datetime(2016, 4, 1))
