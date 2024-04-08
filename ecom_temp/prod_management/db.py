from sqlalchemy import Column, Integer, String, Boolean, BLOB, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from flask_login import UserMixin

Base = declarative_base()

class Products(Base, UserMixin):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    image = Column(BLOB, nullable=False)
    description = Column(String(500), nullable=False)
    name = Column(String(30), nullable=False)
    price = Column(Integer, nullable=False)
    tax = Column(Integer, nullable=False)
    inCart = Column(Boolean, nullable=False)

class Cart(Base, UserMixin):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    # Define other columns as needed

# Use the same create_engine instance for both models
engine = create_engine('sqlite:///product.db')
Base.metadata.create_all(engine)
print("Database created successfully")
