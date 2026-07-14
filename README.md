# PGMS – Personal Growth Management System

## Overview

PGMS (Personal Growth Management System) is a Python application developed following the principles of Clean Architecture. The project aims to help users organize and monitor their personal development by managing goals, habits, daily tasks, and progress in a structured and maintainable way.

The application separates business rules from external technologies, making the code easier to understand, maintain, test, and extend.

---

# Objectives

The main objective of PGMS is to provide a clean and scalable solution for personal productivity while demonstrating the implementation of Clean Architecture in Python.

The project allows users to:

- Create personal goals.
- Track daily habits.
- Manage tasks.
- Monitor progress.
- Organize personal development activities.

---

# Features

- User Management
- Goal Management
- Habit Tracking
- Task Management
- Progress Monitoring
- Data Validation
- Modular Architecture
- Unit Testing

---

# Clean Architecture

The project follows Uncle Bob's Clean Architecture.

```
               Frameworks & Drivers
                       │
              Interface Adapters
                       │
                  Use Cases
                       │
                    Entities
```

Each layer has a single responsibility and depends only on the inner layers.

---

# Project Structure

```
PGMS/
│
├── app/
│   ├── domain/
│   │   ├── entities/
│   │   └── repositories/
│   │
│   ├── use_cases/
│   │
│   ├── interface_adapters/
│   │   ├── controllers/
│   │   ├── presenters/
│   │   └── gateways/
│   │
│   ├── frameworks/
│   │   ├── database/
│   │   ├── cli/
│   │   └── repositories/
│   │
│   └── main.py
│
├── tests/
├── requirements.txt
├── README.md
```

---

# Technologies

- Python 3.11+
- SQLite
- Object-Oriented Programming (OOP)
- Clean Architecture
- SOLID Principles
- unittest

---

# Installation

Clone the repository

```bash
git clone https://github.com/your-username/PGMS.git
```

Move into the project

```bash
cd PGMS
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

macOS/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app/main.py
```

---

# Architecture Benefits

- Independent of frameworks
- Easy to maintain
- Easy to test
- Highly scalable
- Low coupling
- High cohesion
- Better code organization
- Business logic independent from database and UI

---

# Testing

Run all tests

```bash
python -m unittest discover tests
```

---

# Future Improvements

- Authentication
- REST API
- Web Interface
- Mobile Application
- Statistics Dashboard
- Notifications
- Cloud Database
- ⁠
# Author

Chrisnelson Lys

Computer Science Student