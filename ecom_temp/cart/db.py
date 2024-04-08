from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False)


engine = create_engine('sqlite:///product.db')
# Base.metadata.create_all(engine)
print("Database created successfully")