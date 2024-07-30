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

flowchart TD
    A[Customer books a ticket] --> B{Check preferred notification method}
    B -->|Email| C[Send email notification]
    B -->|SMS| D[Send SMS notification]
    C --> E[Store notification in the database]
    D --> E
    E --> F[Ticket created and stored in the database]
    F --> G[Flight status updated]
    G --> H{Check all tickets for the flight}
    H -->|Email| I[Send email notification to all customers]
    H -->|SMS| J[Send SMS notification to all customers]
    I --> K[Update notification status in the database]
    J --> K
