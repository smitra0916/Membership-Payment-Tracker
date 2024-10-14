from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

# Update the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yoyo123:123123@db:5432/postgres_avijoy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define your Member model
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'payment_date': str(self.payment_date)  # Convert date to string
        }

@app.route('/members', methods=['GET', 'POST'])
def members():
    if request.method == 'GET':
        try:
            members = Member.query.all()
            return jsonify([member.to_dict() for member in members]), 200
        except SQLAlchemyError as e:
            return jsonify({"error": "An error occurred while fetching members.", "details": str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            name = data.get('name')
            amount = data.get('amount')
            payment_date = data.get('payment_date')

            if not name or not amount or not payment_date:
                return jsonify({"error": "Missing data in request."}), 400

            # Create a new Member instance
            new_member = Member(name=name, amount=amount, payment_date=payment_date)

            # Add to the session and commit
            db.session.add(new_member)
            db.session.commit()
            return jsonify(new_member.to_dict()), 201

        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the session on error
            return jsonify({"error": "An error occurred while adding a member.", "details": str(e)}), 500
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

@app.route('/members/<int:member_id>', methods=['PUT', 'DELETE'])
def member_detail(member_id):
    try:
        member = Member.query.get_or_404(member_id)

        if request.method == 'PUT':
            data = request.get_json()
            member.name = data.get('name', member.name)
            member.amount = data.get('amount', member.amount)
            member.payment_date = data.get('payment_date', member.payment_date)

            db.session.commit()
            return jsonify(member.to_dict()), 200

        elif request.method == 'DELETE':
            db.session.delete(member)
            db.session.commit()
            return jsonify({"message": "Member deleted successfully."}), 204

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while processing the request.", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
