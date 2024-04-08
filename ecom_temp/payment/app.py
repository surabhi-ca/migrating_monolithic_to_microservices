from flask import Flask, render_template, request
from sqlalchemy.orm import sessionmaker
from db import Base, engine, Payment

app = Flask(__name__)
app.secret_key = "1234"

# Bind the engine to the Base class for declarative
Base.metadata.bind = engine

# Create a sessionmaker to handle database interactions
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/', methods=['GET', 'POST'])
def proceed_to_pay():
    if request.method == 'POST':
        # Handle payment processing logic here
        payment_method = request.form.get('payment_method')
        price = request.form.get('price')
        
        # Create a new Payment object and add it to the database
        new_payment = Payment(payment_method=payment_method, price=price)
        session.add(new_payment)
        session.commit()
        
        return "Payment Successful"  # Redirect or render a success page
    else:
        return render_template('payment.html')

if __name__ == '__main__':
    app.run(debug=True)
