from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Loan Class/Model
class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    interestRate = db.Column(db.Float)
    numberMonths = db.Column(db.Integer)
    monthlyPayment = db.Column(db.Float)

    def __init__(self, amount, interestRate, numberMonths, monthlyPayment):
        self.amount = amount
        self.interestRate = interestRate
        self.numberMonths = numberMonths
        self.monthlyPayment = monthlyPayment

class LoanSchema(ma.Schema):
    class Meta:
        fields = ('id', 'amount', 'interestRate', 'numberMonths', 'monthlyPayment')

loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)

# Create new loan
@app.route('/loan', methods=['POST'])
def add_loan():
    amount = request.json['amount']
    interestRate = request.json['interestRate']
    numberMonths = request.json['numberMonths']
    monthlyPayment = request.json['monthlyPayment']

    new_loan = Loan(amount, interestRate, numberMonths, monthlyPayment)

    db.session.add(new_loan)
    db.session.commit()

    return loan_schema.jsonify(new_loan)

# Get all loans
@app.route('/loan', methods=['GET'])
def get_loans():
    # all_loans = Loan.query.all()
    # result = loans_schema.dump(all_loans)
    # return jsonify(result)

    loan_list = Loan.query.all()
    loans = []

    for loan in loan_list:
        loans.append({'id' : loan.id, "amount" : loan.amount, "interestRate" : loan.interestRate, "numberMonths" : loan.numberMonths, "monthlyPayment" : loan.monthlyPayment})

    return jsonify({'loans' : loans})

# Get single loan
@app.route('/loan/<id>', methods=['GET'])
def get_loan(id):
    loan = Loan.query.get(id)
    return loan_schema.jsonify(loan)

# Update a loan
@app.route('/loan/<id>', methods=['PUT'])
def update_loan(id):
    loan = Loan.query.get(id)

    amount = request.json['amount']
    interestRate = request.json['interestRate']
    numberMonths = request.json['numberMonths']
    monthlyPayment = request.json['monthlyPayment']

    loan.amount = amount
    loan.interestRate = interestRate
    loan.numberMonths = numberMonths
    loan.monthlyPayment = monthlyPayment

    db.session.commit()

    return loan_schema.jsonify(loan)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
