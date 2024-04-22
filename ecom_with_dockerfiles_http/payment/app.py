from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection details
DATABASE_URI = 'sqlite:///product.db'

# Define database table structure
Base = declarative_base()
class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False) 
    name = Column(String(30), nullable=False)
    price = Column(Integer, nullable=False)

class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True)
    payment_method = Column(String(30), nullable=False)
    price = Column(Integer, nullable=False)

# Create the engine and database tables
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

# Create a sessionmaker for database interactions
Session = sessionmaker(bind=engine)

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    session = Session()

    # Retrieve all product IDs from the database
    cart = session.query(Cart).all()
    total_price = session.query(func.sum(Cart.price)).scalar()

# Close the session
    session.close()
    if request.method == 'GET':
    #     session = Session()

    # # Retrieve all product IDs from the database
    #     cart = session.query(Cart).all()
    #     total_price = session.query(func.sum(Cart.price)).scalar()

    # # Close the session
    #     session.close()
        # Render the payment form on GET request
        return render_template('payment.html', data=total_price)
    else:
        # Process form data on POST request

        payment_method = request.form.get('payment_method')
        # price = request.form.get('price')
#############
        # Create a new payment object
        new_payment = Payment(payment_method=payment_method, price=total_price)

        # Create a database session
        session = Session()

        # Add the new payment to the session
        session.add(new_payment)

        # Commit the changes to the database
        session.commit()

        # Close the session
        session.close()

        # Show a success message (or redirect to a success page)
        return "Payment Successful!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
