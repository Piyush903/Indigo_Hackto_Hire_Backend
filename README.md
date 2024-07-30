# Flight Status Notification System

## Project Description

The Flight Status Notification System is a Flask-based application designed to provide real-time flight status updates and notifications to passengers. The system allows users to manage flights, customers, airports, and tickets. Notifications are sent via email or SMS based on the user's preferred notification method.

## Adding Flights and Customers

Flights and customers are added to the database using POST requests. The `/flights` and `/customers` endpoints are used to add flights and customers, respectively.

## Creating Tickets

When a customer books a ticket, a new ticket is created, and a notification is sent based on the customer's preferred notification method. The `/tickets` endpoint is used to create a new ticket.

## Sending Notifications

Notifications are sent when a ticket is created or when a flight status is updated. Notifications can be sent via email or SMS. The notification details are stored in the `notifications` table.

## Flight Status Updates

When the flight status is updated, customers are notified again based on their preferred notification method. The `/flights/<int:flight_id>` endpoint is used to update the flight status.

## Example Notification Email

![Notification Email](https://storage.googleapis.com/image_buck_123/Screenshot%20(16).png)

## API Endpoints

- `GET /flights`: Retrieve all flights.
- `GET /flights/<int:flight_id>`: Retrieve a specific flight by ID.
- `POST /flights`: Add a new flight.
- `PUT /flights/<int:flight_id>`: Update an existing flight.
- `GET /customers`: Retrieve all customers.
- `GET /customers/<int:customer_id>`: Retrieve a specific customer by ID.
- `POST /customers`: Add a new customer.
- `GET /airports`: Retrieve all airports.
- `POST /airports`: Add a new airport.
- `GET /tickets`: Retrieve all tickets.
- `POST /tickets`: Create a new ticket.

## Dependencies

- Flask
- Flask-SQLAlchemy
- Flask-CORS
- Flask-Migrate
- SQLAlchemy
- datetime
- notification_service (Custom module for sending email and SMS notifications)

## Setup

1. Clone the repository.
2. Set up a PostgreSQL database and update the `SQLALCHEMY_DATABASE_URI` in `app.config`.
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
```
4.Run the application:
```
flask run
```
