from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'all_users'
    username = Column(String(100), primary_key=True)
    rate_limit = Column(Integer, nullable=False, default=0)
    register_date = Column(DateTime, nullable=False, default=datetime.datetime.now)

    def print_details(self):
        return_result = {"Username": self.username, "Calls used": self.rate_limit,
                         "Registration date": self.register_date}
        return return_result


engine = create_engine("sqlite:///rate_limiting.db")
Base.metadata.create_all(engine)
