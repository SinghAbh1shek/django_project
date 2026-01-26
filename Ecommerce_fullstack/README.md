# E-Commerce Web Application (Django)

A scalable, role-based E-Commerce web application built using Python and Django.  
The platform supports customers and sellers with secure payments, background processing, caching, and fast product search.

This project demonstrates real-world backend development practices including payment gateway integration, asynchronous task processing, caching, and search optimization.

---

## Features

### Authentication and Roles
- User authentication and authorization
- Role-based access for Customers and Sellers
- Seller onboarding and dashboard management

### Google Authentication and Profile Sync

- Implemented **Login with Google** using OAuth 2.0
- Automatically retrieves user profile details such as name, email, and profile image from Google
- Creates and updates the application user profile using Google account data
- Provides a seamless sign-up and login experience without manual form filling


### Product and Order Management
- Product creation, listing, and inventory management
- Shopping cart and checkout workflow
- Order placement, and order history

### Payment Integration
- Secure payment processing using Razorpay
- Payment verification and transaction status handling
- Order confirmation after successful payment

### Performance and Scalability
- Redis caching to reduce database queries and improve response times
- Celery with Redis for asynchronous background task execution
- Background processing for PDF invoice generation

### Search
- Elasticsearch integration for fast, full-text product search
- Efficient filtering across the product catalog

### Admin Management
- Django Admin for backend operations and data management
- Modular app structure following Django best practices

---

## Tech Stack

### Backend
- Python
- Django
- Django ORM

### Database
- PostgreSQL

### Async and Caching
- Redis
- Celery

### Search
- Elasticsearch

### Payments
- Razorpay API

### Frontend
- HTML5
- CSS3
- Bootstrap
- JavaScript

### Tools
- Git
- UV (Python package manager)

---

## Project Structure

<pre>
Ecommerce_fullstack/
├── accounts/
├── core/
├── home/
├── media/
├── orders/
├── products/
├── profiles/
├── seller/
├── static/
├── utils/
├── .env
├── manage.py
├── pyproject.toml
├── uv.lock
└── README.md
</pre>

---

## Installation and Setup

Clone the repository
git clone https://github.com/SinghAbh1shek/django_project.git
cd django_project

Create and Activate Virtual Environment (UV)

Initiallize UV Environment:
* uv init .

## Environment Variables

This project uses environment variables for configuration.  
A sample environment file is provided as `.env.example`.

## Running the Project Locally

Install dependencies using UV
* uv sync

Apply database migrations
* uv run manage.py makemigrations
* uv run manage.py migrate

Create superuser for admin access
* uv run manage.py createsuperuser

Start Redis server
redis-server

Ensure Elasticsearch is running locally on port 9200

Start Celery worker:
* uv run celery -A core worker -l info

Run the Django development server
* uv run manage.py runserver

Application URL
http://127.0.0.1:8000/

Admin Panel
http://127.0.0.1:8000/admin/

---

## Background Tasks

Celery with Redis is used for:
- PDF invoice generation
- Long-running background tasks

---

## Performance Optimizations

- Redis caching for frequently accessed data
- Asynchronous processing using Celery
- Optimized database queries using Django ORM
- Elasticsearch for low-latency search

---

## Future Enhancements

- Django REST Framework APIs
- JWT authentication
- Product reviews and ratings
- Dockerized deployment
- React frontend
- Cloud deployment

---

## Author

Abhishek Singh  
Python and Django Developer  

GitHub: https://github.com/SinghAbh1shek    

---

## License

This project is created for learning and portfolio purposes.  
Free to use and modify for educational use.
