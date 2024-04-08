from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import Column, Integer, String, Boolean, BLOB, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "1234"

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

# Use the same create_engine instance for both models
engine = create_engine('sqlite:///product.db')
Base.metadata.create_all(engine)
print("Database created successfully")

engine = create_engine('sqlite:///product.db', connect_args={'check_same_thread': False}, echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base.metadata.bind = engine

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

@app.route('/', methods=['GET', 'POST'])
@app.route('/product', methods=['GET', 'POST'])
def viewProducts():
    dbData = session.query(Products).all()
    for i in dbData:
        no = "photo" + str(i.id)
        write_file(i.image, "static/images" + no + ".jpg")
    return render_template('index.html', data=dbData)

@app.route('/<int:r_id>/view', methods=['GET', 'POST'])
def viewDetails(r_id):
    dbData = session.query(Products).all()
    return render_template('viewDetails.html', id=r_id, details=dbData)

@app.route('/<int:r_id>/sample', methods=['GET', 'POST'])
def sample(r_id):
    # Fetch all products
    dbData = session.query(Products).all()

    # Fetch the product to update
    update_this = session.query(Products).filter_by(id=r_id).first()

    if request.method == 'POST':
        # Check if the product is already in the cart
        product_in_cart = session.query(Cart).filter_by(product_id=r_id).first()

        if product_in_cart:
            flash('Product already added to cart!', 'warning')
        else:
            # Append the product ID to the cart
            cart_product = Cart(product_id=r_id)
            session.add(cart_product)
            session.commit()
            flash('Product added to cart successfully!', 'success')

        # Redirect to the same route to avoid form resubmission
        return redirect(url_for('sample', r_id=r_id))

    # Toggle the 'inCart' status of the product
    update_this.inCart = not update_this.inCart
    session.commit()

    return render_template('viewDetails.html', id=r_id, details=dbData)

if __name__ == '__main__':
    app.run(debug=True)
