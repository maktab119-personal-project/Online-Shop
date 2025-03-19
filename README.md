# Online-Shop Project

## Overview
This project is an online store web application built using Django. It includes key e-commerce functionalities such as product management, customer accounts, order processing, and an admin panel for managing store operations.

## Features
- **User Management**: Customers can register, log in, and manage their accounts.
- **Product Management**: Store managers can add, edit, and categorize products.
- **Shopping Cart & Orders**: Customers can add products to a cart and place orders.
- **Admin Panel**: Admins can oversee store operations, manage products, and view customer orders.
- **Discount System**: Supports percentage-based and fixed-amount discounts.
- **Category Hierarchy**: Products are categorized in a tree-structured manner.
- **Authentication**: Supports login via email with OTP or username and password.
- **Order Tracking**: Customers can track their past and current orders.

## Technologies Used
- **Backend**: Django & Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Frontend**: Django Templates (Bootstrap/Tailwind for styling)
- **Caching**: Redis (for OTP authentication)
- **Version Control**: Git & GitHub

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Online-Shop
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the server:
   ```bash
   python manage.py runserver
   ```
7. Access the application at `http://127.0.0.1:8000/`

## Project Structure
```
project_root/
│── core/              # Core utilities & base models
│── customers/         # Customer-related functionality
│── products/         # Product & category management
│── orders/           # Order & cart management
│── templates/        # Frontend templates
│── static/           # Static assets (CSS, JS, images)
│── manage.py         # Django management script
│── requirements.txt  # Python dependencies
│── README.md         # Project documentation
```

## Development Workflow
- Use **feature branches** for new features.
- Follow **GitFlow** with `develop` and `main` branches.
- All commits must be pushed to GitHub before deadlines.

## Testing & Coverage
- Ensure **80%+ test coverage** using Django’s testing framework.
- Selenium is used for end-to-end testing.

## Contributors
- Other contributors listed in GitHub repository.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any inquiries, contact the project owner via GitHub issues or email.

