import random
import time
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customerStay.db'
db = SQLAlchemy(app)
reservations = []

class CustomerStay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    start_date = db.Column(db.String(80), nullable=False)
    end_date = db.Column(db.String(80), nullable=False)
    room_type = db.Column(db.String(80), nullable=False)
    confirmation_number = db.Column(db.String(10), nullable=False)


def create_db():
    with app.app_context():
        db.create_all()


create_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        room_type = request.form['room_type']

        # Generate a random confirmation number
        confirmation_number = ''.join(random.choices('0123456789', k=6))

        new_stay = CustomerStay(first_name=first_name, last_name=last_name, start_date=start_date,
                                end_date=end_date, room_type=room_type, confirmation_number=confirmation_number)
        db.session.add(new_stay)
        db.session.commit()

        # Retrieve all customer stays
        customerInfo = CustomerStay.query.all()

        # Retrieve the newly added customer stay for the confirmation summary
        new_stay_summary = CustomerStay.query.filter_by(confirmation_number=confirmation_number).first()

    return render_template('make_reservation.html', time=time)


@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    room_types = ['Single', 'Double', 'King', 'Queen']  # Define room types
    if request.method == 'POST':
        # Process the form data to create a new reservation

        # Placeholder reservation data for demonstration
        reservation = {
            'confirmation_number': 'ABC123',
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'date': request.form['start_date']
        }

        reservations.append(reservation)  # Add the reservation to the list


        return render_template('make_reservation.html', room_types=room_types)

    return render_template('make_reservation.html', room_types=room_types, tab='make_reservation')


@app.route('/view_reservation', methods=['GET', 'POST'])
def view_reservation():
    if request.method == 'POST':
        confirmation_number = request.form['confirmation_number']

        # Search for the reservation based on the confirmation number
        reservation = None
        for res in reservations:
            if res['confirmation_number'] == confirmation_number:
                reservation = res
                break

        if reservation:
            return render_template('reservation_details.html', reservation=reservation)
        else:
            error_message = "Reservation not found. Please check your confirmation number."
            return render_template('error.html', error_message=error_message)

    return render_template('view_reservation.html', tab='view_reservation')


@app.route('/modify_reservation', methods=['GET', 'POST'])
def modify_reservation():
    if request.method == 'POST':
        confirmation_number = request.form['confirmation_number']

        # Search for the reservation based on the confirmation number
        reservation = None
        for res in reservations:
            if res['confirmation_number'] == confirmation_number:
                reservation = res
                break

        if reservation:
            return render_template('modify_reservation.html', reservation=reservation)
        else:
            error_message = "Reservation not found. Please check your confirmation number."
            return render_template('error.html', error_message=error_message)

    return render_template('modify_reservation.html', tab='modify_reservation')


# Process the cancellation of the reservation
@app.route('/cancel_reservation', methods=['GET', 'POST'])
def cancel_reservation():
    if request.method == 'POST':
        # success response
        success_message = "Reservation canceled successfully."
        return render_template('cancel_reservation_success.html', success_message=success_message)

    return render_template('cancel_reservation.html', tab='cancel_reservation')


if __name__ == '__main__':
    app.run()
