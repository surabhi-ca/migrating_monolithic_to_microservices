from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
# Database connection details
DATABASE_URI = 'sqlite:///product.db'
PRODUCT_MANAGEMENT_HOST = 'http://localhost'  # Replace 'your_node_ip' with the IP address of your Kubernetes node
PRODUCT_MANAGEMENT_PORT = 32000 
# Define database table structure (using plain text password storage - NOT RECOMMENDED)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)

# Create the engine and database tables (if they don't exist)
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

# Create a sessionmaker for database interactions
Session = sessionmaker(bind=engine)

app = Flask(__name__, template_folder='templates')
app.secret_key = '123'  # Add a secret key for session management

@app.route('/', methods=['GET', 'POST'])  # Signup route at the root URL (handles GET and POST)
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Create a database session
        session = Session()

        # Check if username already exists
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!', 'danger')
            session.close()
            return redirect(url_for('signup'))

        # Create a new user object
        new_user = User(username=username, password=password)  # Plain text password storage (NOT RECOMMENDED)

        # Add the new user to the database
        session.add(new_user)
        session.commit()
        session.close()

        flash('Signup successful!', 'success')
        return redirect(url_for('signup'))  # Redirect to signup page after successful registration (can be changed)

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])  # Login route
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Create a database session
        session = Session()

        # Check if user exists
        user = session.query(User).filter_by(username=username).first()
        session.close()

        if user and user.password == password:  # Plain text password comparison (NOT RECOMMENDED)
            # Login successful, print message or redirect
            print("Login successful!")  # Print success message to the console
            flash('Login successful!', 'success')
            return redirect(f'http://localhost:32000')
        # Redirect the user to the product page
                #return redirect(f'http://{PRODUCT_MANAGEMENT_HOST}:{PRODUCT_MANAGEMENT_PORT}')  # Optionally, flash a success message for the user
            # return redirect(url_for('index'))  # Replace with desired location after login (commented out)
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
