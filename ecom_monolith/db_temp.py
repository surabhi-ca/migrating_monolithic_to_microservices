from sqlalchemy import Column, Integer, String, Boolean, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    image = Column(BLOB, nullable=False)
    description = Column(String(500), nullable=False)
    name = Column(String(30), nullable=False)
    price = Column(Integer, nullable=False)
    tax = Column(Integer, nullable=False)
    inCart = Column(Boolean, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

engine = create_engine('sqlite:///product.db')
Base.metadata.create_all(engine)
print("Database created successfully")
