from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update with your database connection details
DATABASE_URL = 'sqlite:///payments.db'

app = Flask(__name__)

# Define database table schema
Base = declarative_base()

class Payment(Base):
  __tablename__ = 'payments'
  id = Column(Integer, primary_key=True)
  serial_no = Column(String, unique=True)
  members = Column(String)
  payment_amount = Column(Float)
  date_of_payment = Column(Date)
  earlier_amount = Column(Float)

# Connect to database
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Create session for database interaction
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/payments', methods=['POST'])
def add_payment():
  data = request.get_json()
  new_payment = Payment(
      serial_no=data['serial_no'],
      members=data['members'],
      payment_amount=data['payment_amount'],
      date_of_payment=data['date_of_payment'],
      earlier_amount=data['earlier_amount'],
  )
  session.add(new_payment)
  session.commit()
  return jsonify({'message': 'Payment added successfully'}), 201

# Add additional routes for retrieving, updating, or deleting payments

if __name__ == '__main__':
  app.run(debug=True)