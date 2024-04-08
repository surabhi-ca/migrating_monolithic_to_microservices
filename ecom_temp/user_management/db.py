from sqlalchemy import Column, Integer, String, Boolean, BLOB, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from flask_login import UserMixin

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)


# Use the same create_engine instance for both models
engine = create_engine('sqlite:///product.db')
Base.metadata.create_all(engine)
print("Database created successfully")
