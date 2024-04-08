from flask import Flask, render_template, request, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base,  Cart

app = Flask(__name__)

# Connect to the database
engine = create_engine('sqlite:///payment.db')
Base.metadata.bind = engine

# Create a session
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/', methods=['GET', 'POST'])
def view_cart():

    # Fetch items from the Cart table
    cart_items = session.query(Cart).all()
    return render_template('cart.html', cart_items=cart_items)


if __name__ == '__main__':
    app.run(debug=True)


