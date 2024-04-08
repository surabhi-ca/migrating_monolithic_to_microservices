from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, User

import sys
sys.path.append("D:/cc_proj_flask/ecom_temp")  # Adjust the path accordingly
# from product_management.db import Products, Cart

# from product_management.app import app


app = Flask(__name__)
app.secret_key = '123'  # Change this to a secret key of your choice

engine = create_engine('sqlite:///D:/cc_proj_flask/ecom_temp/product.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            # User authenticated, redirect to home page or dashboard
            flash('Login successful!', 'success')
            # return redirect(url_for('login'))
            return redirect(url_for('login'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username already exists
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('signup'))
        else:
            # Create new user
            username = request.form.get('username')
            password = request.form.get('password')
            new_user = User(username=username, password=password)
            session.add(new_user)
            session.commit()
            flash('Account created successfully! You can now log in', 'success')
            print("user added")
            return redirect(url_for('login'))
    return render_template('signup.html')



if __name__ == '__main__':
    app.run(debug=True)
