from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from db import Base, Products, User

app = Flask(__name__)
app.secret_key = "1234"

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

engine = create_engine('sqlite:///product.db', connect_args={'check_same_thread': False}, echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base.metadata.bind = engine

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

@app.route('/', methods=['GET', 'POST'])
def viewProducts():
    dbData = session.query(Products).all()
    for i in dbData:
        no = "photo" + str(i.id)
        write_file(i.image, "static/images" + no + ".jpg")
    return render_template('index.html', data=dbData)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        imageData = request.files['image']
        if not imageData:
            return 'No pic uploaded!', 400
        img = Products(image=imageData.read(),
                       name=request.form['name'],
                       description=request.form['description'],
                       price=request.form['price'],
                       tax=request.form['tax'],
                       inCart=False)
        session.add(img)
        session.commit()
        return redirect(url_for('viewProducts'))
    return render_template('admin.html')

@app.route('/<int:r_id>/view', methods=['GET', 'POST'])
def viewDetails(r_id):
    dbData = session.query(Products).all()
    return render_template('viewDetails.html', id=r_id, details=dbData)

@app.route('/<int:r_id>/cart', methods=['GET', 'POST'])
def viewCart(r_id):
    if r_id != 0:
        update = session.query(Products).filter_by(id=r_id).first()
        update.inCart = False
        session.commit()
    dbData = session.query(Products).all()
    flag = False
    total = 0
    for i in dbData:
        if i.inCart == True:
            total += (i.price + i.tax)
            flag = True
    return render_template('viewCart.html', details=dbData, flag=flag, total=total)

@app.route('/<int:r_id>/sample', methods=['GET', 'POST'])
def sample(r_id):
    dbData = session.query(Products).all()
    update_this = session.query(Products).filter_by(id=r_id).first()
    if update_this.inCart == True:
        update_this.inCart = False
    else:
        update_this.inCart = True
    session.commit()
    return render_template('viewDetails.html', id=r_id, details=dbData)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('viewProducts'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            session.add(new_user)
            session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('viewProducts'))

if __name__ == "__main__":
    app.run(debug=True)
