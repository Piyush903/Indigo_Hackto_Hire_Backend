from flask import Flask, request, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from flask_migrate import Migrate
from notification_service import send_email, send_sms
from sqlalchemy.orm import aliased
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/flight_status'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# Define models
class Airport(db.Model):
    __tablename__ = 'airports'
    airport_id = db.Column(db.Integer, primary_key=True)
    iata_code = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    timezone = db.Column(db.String(50))

class Flights(db.Model):
    flight_id = db.Column(db.Integer, primary_key=True)
    flight_date = db.Column(db.Date, nullable=False)
    flight_status = db.Column(db.String(50), nullable=False)
    departure_airport_id = db.Column(db.Integer, db.ForeignKey('airports.airport_id'))
    arrival_airport_id = db.Column(db.Integer, db.ForeignKey('airports.airport_id'))
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    airline = db.Column(db.String(100))
    delay = db.Column(db.Integer)
    departure_airport = db.relationship('Airport', foreign_keys=[departure_airport_id])
    arrival_airport = db.relationship('Airport', foreign_keys=[arrival_airport_id])


class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    preferred_notification_method = db.Column(db.String(50))

class Notification(db.Model):
    __tablename__ = 'notifications'
    notification_id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.flight_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    notification_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    sent_at = db.Column(db.DateTime)
    recipient = db.Column(db.String(100), nullable=False)

class Ticket(db.Model):
    __tablename__ = 'tickets'
    ticket_id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.flight_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.notification_id'))
    created_at = db.Column(db.DateTime, default=datetime.now)

# Serialization methods
def serialize_flight(flight):
    return {
        'flight_id': flight.flight_id,
        'flight_date': flight.flight_date.isoformat(),
        'flight_status': flight.flight_status,
        'departure_airport_id': flight.departure_airport_id,
        'departure_airport_name': flight.departure_airport.name,
        'arrival_airport_id': flight.arrival_airport_id,
        'arrival_airport_name': flight.arrival_airport.name,
        'departure_time': flight.departure_time.isoformat(),
        'arrival_time': flight.arrival_time.isoformat(),
        'airline': flight.airline,
        'delay': flight.delay
    }

def serialize_customer(customer):
    return {
        'customer_id': customer.customer_id,
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone,
        'preferred_notification_method': customer.preferred_notification_method
    }

def serialize_notification(notification):
    return {
        'notification_id': notification.notification_id,
        'flight_id': notification.flight_id,
        'customer_id': notification.customer_id,
        'notification_type': notification.notification_type,
        'status': notification.status,
        'sent_at': notification.sent_at.isoformat() if notification.sent_at else None,
        'recipient': notification.recipient
    }

def serialize_ticket(ticket):
    return {
        'ticket_id': ticket.ticket_id,
        'flight_id': ticket.flight_id,
        'customer_id': ticket.customer_id,
        'notification_id': ticket.notification_id,
        'created_at': ticket.created_at.isoformat()
    }

# API endpoints
@app.route('/flights', methods=['GET'])
def get_flights():
    flights = Flights.query.all()
    return jsonify([serialize_flight(flight) for flight in flights])

@app.route('/flights/<int:flight_id>', methods=['GET'])
def get_flight(flight_id):
    flight = Flights.query.get_or_404(flight_id)
    return jsonify(serialize_flight(flight))
    
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customers.query.get_or_404(customer_id)
    return jsonify(serialize_customer(customer))

@app.route('/airports', methods=['GET'])
def get_airports():
    airports = Airport.query.all()
    return jsonify([{
        'airport_id': airport.airport_id,
        'iata_code': airport.iata_code,
        'name': airport.name,
        'city': airport.city,
        'country': airport.country,
        'timezone': airport.timezone
    } for airport in airports])

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([serialize_customer(customer) for customer in customers])

@app.route('/tickets', methods=['GET'])
def get_tickets():
    tickets = Ticket.query.all()
    return jsonify([serialize_ticket(ticket) for ticket in tickets])

@app.route('/tickets', methods=['POST'])
def create_ticket():
    customer_id = request.form.get('customer_id')
    flight_id = request.form.get('flight_id')

    customer = Customer.query.get_or_404(customer_id)
    
    DepartureAirport = aliased(Airport, name='departure_airport')
    ArrivalAirport = aliased(Airport, name='arrival_airport')
    
    flight = db.session.query(Flights).join(
        DepartureAirport, Flights.departure_airport_id == DepartureAirport.airport_id
    ).join(
        ArrivalAirport, Flights.arrival_airport_id == ArrivalAirport.airport_id
    ).filter(
        Flights.flight_id == flight_id
    ).first()

    notification_type = customer.preferred_notification_method

    # Create the notification
    notification = Notification(
        flight_id=flight_id,
        customer_id=customer_id,
        notification_type=notification_type,
        status='sent',
        sent_at=datetime.now(),
        recipient=customer.email if notification_type == 'email' else customer.phone
    )
    db.session.add(notification)
    db.session.commit()

    # Create the ticket
    ticket = Ticket(
        flight_id=flight_id,
        customer_id=customer_id,
        notification_id=notification.notification_id
    )
    db.session.add(ticket)
    db.session.commit()

    # Send the notification based on flight status
    if flight.flight_status == 'scheduled':
        email_body = render_template('email_template.html', flight=serialize_flight(flight), customer=serialize_customer(customer))
        if notification_type == 'email':
            send_email(customer.email, 'Flight Status Update', email_body)
        elif notification_type == 'sms':
            send_sms(customer.phone, f'Your flight status is scheduled')
    else:
        if notification_type == 'email':
            send_email(customer.email, 'Flight Status Update', f'Your flight status is {flight.flight_status}')
        elif notification_type == 'sms':
            send_sms(customer.phone, f'Your flight status is {flight.flight_status}')

    return jsonify(serialize_ticket(ticket)), 201


@app.route('/flights', methods=['POST'])
def add_flight():
    data = request.form
    flight = Flights(
        flight_date=data['flight_date'],
        flight_status=data['flight_status'],
        departure_airport_id=data['departure_airport_id'],
        arrival_airport_id=data['arrival_airport_id'],
        departure_time=data['departure_time'],
        arrival_time=data['arrival_time'],
        airline=data.get('airline'),
        delay=data.get('delay', 0)
    )
    db.session.add(flight)
    db.session.commit()
    return jsonify(serialize_flight(flight)), 201

@app.route('/flights/<int:flight_id>', methods=['PUT'])
def update_flight(flight_id):
    flight = Flights.query.get_or_404(flight_id)
    data = request.form
    flight.flight_status = data.get('flight_status', flight.flight_status)
    flight.delay = data.get('delay', flight.delay)
    db.session.commit()

    # Notify customers about the flight status update
    notify_customers_on_flight_update(flight_id)

    return jsonify(serialize_flight(flight))

@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.form
    customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        preferred_notification_method=data['preferred_notification_method']
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify(serialize_customer(customer)), 201

@app.route('/airports', methods=['POST'])
def add_airport():
    data = request.form
    airport = Airport(
        iata_code=data['iata_code'],
        name=data['name'],
        city=data['city'],
        country=data['country'],
        timezone=data.get('timezone')
    )
    db.session.add(airport)
    db.session.commit()
    return jsonify({
        'airport_id': airport.airport_id,
        'iata_code': airport.iata_code,
        'name': airport.name,
        'city': airport.city,
        'country': airport.country,
        'timezone': airport.timezone
    }), 201


def notify_customers_on_flight_update(flight_id):
    DepartureAirport = aliased(Airport, name='departure_airport')
    ArrivalAirport = aliased(Airport, name='arrival_airport')

    flight = db.session.query(Flights).join(
        DepartureAirport, Flights.departure_airport_id == DepartureAirport.airport_id
    ).join(
        ArrivalAirport, Flights.arrival_airport_id == ArrivalAirport.airport_id
    ).filter(
        Flights.flight_id == flight_id
    ).first()

    tickets = Ticket.query.filter_by(flight_id=flight_id).all()

    for ticket in tickets:
        customer = Customer.query.get(ticket.customer_id)
        notification_type = customer.preferred_notification_method

        # Send notification based on flight status
        if flight.flight_status == 'scheduled':
            email_body = render_template('email_template.html', flight=serialize_flight(flight), customer=serialize_customer(customer))
            if notification_type == 'email':
                send_email(customer.email, 'Flight Status Update', email_body)
            elif notification_type == 'sms':
                send_sms(customer.phone, f'Your flight status is scheduled')
        else:
            if notification_type == 'email':
                send_email(customer.email, 'Flight Status Update', f'Your flight status is {flight.flight_status}')
            elif notification_type == 'sms':
                send_sms(customer.phone, f'Your flight status is {flight.flight_status}')

        # Create a new notification entry
        notification = Notification(
            flight_id=flight_id,
            customer_id=customer.customer_id,
            notification_type=notification_type,
            status='sent',
            sent_at=datetime.now(),
            recipient=customer.email if notification_type == 'email' else customer.phone
        )
        db.session.add(notification)
        db.session.commit()
