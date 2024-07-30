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
# Flight Status Notification System

This project is a Flask application designed to provide real-time flight status updates and notifications to passengers. Notifications are sent via email or SMS based on the user's preferred notification method.

## System Design

### Database Schema

The system consists of the following tables:

- **airports**: Stores information about airports.
- **flights**: Stores information about flights.
- **customers**: Stores information about customers.
- **notifications**: Stores information about notifications sent to customers.
- **tickets**: Stores information about tickets booked by customers.

```mermaid
erDiagram
    AIRPORTS {
        int airport_id PK
        string iata_code
        string name
        string city
        string country
        string timezone
    }
    FLIGHTS {
        int flight_id PK
        date flight_date
        string flight_status
        int departure_airport_id FK
        int arrival_airport_id FK
        datetime departure_time
        datetime arrival_time
        string airline
        int delay
    }
    CUSTOMERS {
        int customer_id PK
        string name
        string email
        string phone
        string preferred_notification_method
    }
    NOTIFICATIONS {
        int notification_id PK
        int flight_id FK
        int customer_id FK
        string notification_type
        string status
        datetime sent_at
        string recipient
    }
    TICKETS {
        int ticket_id PK
        int flight_id FK
        int customer_id FK
        int notification_id FK
        datetime created_at
    }

    FLIGHTS ||--o{ AIRPORTS: "departure_airport_id"
    FLIGHTS ||--o{ AIRPORTS: "arrival_airport_id"
    NOTIFICATIONS ||--o{ FLIGHTS: "flight_id"
    NOTIFICATIONS ||--o{ CUSTOMERS: "customer_id"
    TICKETS ||--o{ FLIGHTS: "flight_id"
    TICKETS ||--o{ CUSTOMERS: "customer_id"
    TICKETS ||--o{ NOTIFICATIONS: "notification_id"


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
4.Run the application:
  ```sh
  flask run

