from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

import hashlib

Base = declarative_base()


class User(Base):
    __tablename__ = 'all_users'
    username = Column(String(100), primary_key=True)
    password = Column(String(300), nullable=False)

    def hash_password(self):
        self.password = str(hashlib.sha3_256(self.password.encode()).hexdigest())

    def verify_password(self, password):
        if self.password == hashlib.sha3_256(password.encode()).hexdigest():
            return True
        else:
            return False

    def print_details(self):
        return self.username + " -> " + self.password


engine = create_engine("sqlite:///users.db")
Base.metadata.create_all(engine)
