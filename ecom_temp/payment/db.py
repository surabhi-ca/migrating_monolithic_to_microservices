from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True)
    payment_method = Column(String(30), nullable=False)
    price = Column(Integer, nullable=False)

engine = create_engine('sqlite:///D:/cc_proj_flask/ecom_temp/product.db')
Base.metadata.create_all(engine)
print("Database created successfully")