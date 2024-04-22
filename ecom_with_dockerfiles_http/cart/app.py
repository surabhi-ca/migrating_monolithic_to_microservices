from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Database connection details
DATABASE_URI = 'sqlite:///product.db'

# Define database table structure (assuming a table named 'products')
Base = declarative_base()

class Product(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, nullable=False) 
    name = Column(String(30), nullable=False)
    price = Column(Integer, nullable=False)

# Create the engine and database tables (if they don't exist)
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

# Create a sessionmaker for database interactions
Session = sessionmaker(bind=engine)

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['POST','GET'])
def index():
    # Create a database session
    session = Session()

    # Retrieve all product IDs from the database
    products = session.query(Product).all()

    # Close the session
    session.close()
    if request.method == 'POST':
        return redirect(f'http://localhost:30021')
    # Pass the list of products to the template for rendering
    return render_template('cart.html', cart_items=products)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')