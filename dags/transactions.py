from sqlalchemy import Integer, ForeignKey, Column, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dags.users import User
from session import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    price = Column(Float, nullable=False)

    user = relationship("User", backref="transactions")