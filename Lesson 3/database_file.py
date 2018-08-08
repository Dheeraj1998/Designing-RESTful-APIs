from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

table_engine = create_engine('sqlite:///restaurants.db')
Base = declarative_base()


class RestaurantInfo(Base):
    __tablename__ = 'restaurant_info'

    name = Column(String(250), primary_key=True)
    address = Column(String(250), nullable=False)


Base.metadata.create_all(table_engine)
