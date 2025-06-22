# HBnB Evolution (part2) – Implementation of Business Logic and API Endpoints

## Overview

This part of the **HBnB Evolution** project establishes the foundational structure of the application using a **layered architecture** with the **Facade pattern**. The setup prepares the system for future integration of business logic, API endpoints, and database support.

The project is organized into three primary layers:
- **Presentation Layer** – API endpoints exposed to users
- **Business Logic Layer** – Core functionality and data models
- **Persistence Layer** – In-memory repository for storing and retrieving objects (replacing database for now)

## Python Dependencies

Install dependencies by copying **requirements.txt** file and running:

`pip install -r requirements.txt`

requirements.txt should contain this:

- `flask`
- `flask-restx`

---

## Business Logic Layer

This layer implements the core entities for the HBnB system. Each class inherits from a shared `BaseModel` that provides a unique ID and timestamp tracking.

### Implemented Classes:

- `User`: Stores user info and permissions.
- `Place`: Represents properties listed by users.
- `Review`: Contains user-submitted reviews for places.
- `Amenity`: Represents features like Wi-Fi, Parking, etc.

### Sample Code:

```python
from app.models.user import User
user = User("John", "Doe", "john@example.com")
```

---

## Directory Structure

```text
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py  
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   ├── persistence/
│       ├── __init__.py
│       └── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
