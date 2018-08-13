from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

import hashlib
import random
import string

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))


class User(Base):
    __tablename__ = 'all_users'
    username = Column(String(100), primary_key=True)
    password = Column(String(300), nullable=False)

    def hash_password(self):
        self.password = str(hashlib.sha3_256(self.password.encode()).hexdigest())

    def verify_password(self, password):
        if hashlib.sha3_256(password.encode()).hexdigest() == self.password:
            return True
        else:
            return False

    def print_details(self):
        return self.username + " -> " + self.password
        
    def generate_token(self, expiration=100):
        serializer = Serializer(secret_key, expires_in=expiration)
        token_value = serializer.dumps({'username': self.username})
        print(secret_key)
        return token_value

    @staticmethod
    def verify_token(token_value):
        serializer = Serializer(secret_key)
        print(secret_key)
        try:
            data = serializer.loads(token_value)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        username = data['username']
        return {"message": "The token is valid.", "Username": username}


engine = create_engine("sqlite:///users.db")
Base.metadata.create_all(engine)
