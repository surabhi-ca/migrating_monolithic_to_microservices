from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, Integer, String,BLOB,Boolean,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, redirect, flash, render_template, url_for  # Other imports you might need

# Configure database connection

DATABASE_URI = 'sqlite:///product.db'


Base = declarative_base()
# Define product model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    image = Column(BLOB, nullable=False)
    description = Column(String(500), nullable=False)
    name = Column(String(30), nullable=False)
    price = Column(Integer, nullable=False)
    tax = Column(Integer, nullable=False)
    inCart = Column(Boolean, nullable=False)

# Define cart model with explicit table name (if implemented)
class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    # Add other cart-related columns if needed (quantity, size, etc.)

# Create database tables if they don't exist (one-time setup)
# @app.before_app_first_request
# def create_tables():
#     db.create_all()
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

# Create a sessionmaker for database interactions
Session = sessionmaker(bind=engine)

app = Flask(__name__, template_folder='templates')
app.secret_key = "123"

@app.route('/')
def index():
    # Fetch all products from the database
    session = Session()

    # Retrieve all product IDs from the database
    products = session.query(Product).all()

    # Close the session
    session.close()
    return render_template('index.html', data=products)

@app.route('/product')
def viewProducts():
    # Alternative route to display products (optional)
    # You can use the same logic as in index()
    session = Session()

    # Retrieve all product IDs from the database
    products = session.query(Product).all()

    # Close the session
    session.close()
    return render_template('index.html', data=products)

@app.route('/<int:r_id>/view', methods=['GET', 'POST'])
def viewDetails(r_id):
    with Session() as session:
        product = session.query(Product).get(r_id)
        if product is None:
            flash('Product not found!', category='error')
            return redirect(url_for('index'))
    

    return render_template('viewDetails.html', product=product)


@app.route('/<int:r_id>/sample', methods=['GET', 'POST'])
def addToCart(r_id):
    with Session() as session:  # Create and close session automatically
        # Retrieve product details based on product ID
        product = session.query(Product).get(r_id)

        if product is None:
            flash('Product not found!', category='error')
            return redirect(url_for('index'))

        # Check if product already exists in cart (using session)
        if session.query(Cart).filter_by(product_id=r_id).first() is not None:
            flash('Product already exists in cart!', category='warning')
            return redirect(url_for('viewDetails', r_id=r_id))

        # Add product to cart
        new_cart_item = Cart(product_id=product.id)
        session.add(new_cart_item)
        session.commit()
        flash('Product added to cart!', category='success')
        return redirect(url_for('viewDetails', r_id=r_id))

# Define a Cart model if you want to implement cart functionality (optional)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
