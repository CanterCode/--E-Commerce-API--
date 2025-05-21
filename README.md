# 🛒 E-Commerce API

A fully functional RESTful API built with **Flask**, **SQLAlchemy**, **Marshmallow**, and **MySQL** to manage users, products, and orders for an e-commerce application. I used ChatGPT and CoPilot to assist in debugging, creating, and organizing.

---

## 🚀 Project Overview

This API allows you to:
- Manage **Users**, **Products**, and **Orders**
- Establish relationships:  
  - One-to-Many: A User can have many Orders  
  - Many-to-Many: An Order can contain many Products, and vice versa
- Serialize and validate data using **Marshmallow**
- Interact with a **MySQL** database using **Flask-SQLAlchemy**

---

## 🛠️ Tools & Technologies
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow / Marshmallow-SQLAlchemy
- MySQL
- Postman
- MySQL Workbench

---

## 📬 API Endpoints

### 🧑 Users
- `GET /users` - Retrieve all users  
- `GET /users/<id>` - Retrieve a user by ID  
- `POST /users` - Create a new user  
- `PUT /users/<id>` - Update a user by ID  
- `DELETE /users/<id>` - Delete a user by ID  

### 📦 Products
- `GET /products` - Retrieve all products  
- `GET /products/<id>` - Retrieve a product by ID  
- `POST /products` - Create a new product  
- `PUT /products/<id>` - Update a product by ID  
- `DELETE /products/<id>` - Delete a product by ID  

### 🧾 Orders
- `POST /orders` - Create a new order  
- `PUT /orders/<order_id>/add_product/<product_id>` - Add a product to an order  
- `DELETE /orders/<order_id>/remove_product` - Remove a product from an order  
- `GET /orders/user/<user_id>` - Get all orders for a specific user  
- `GET /orders/<order_id>/products` - Get all products in a specific order

---

## ▶️ How to Run the App

- Clone the repository to your local machine
- Navigate to the project directory
- Create a virtual environment  
  `python -m venv venv`
- Activate the virtual environment  
  - Windows: `venv\Scripts\activate`  
  - macOS/Linux: `source venv/bin/activate`
- Install dependencies  
  `pip install -r requirements.txt`
- Make sure MySQL is running and the `ecommerce_api` database is created
  `app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:<YOUR_PASSWORD>@localhost/ecommerce_api'`
- Run the Flask app  
  `flask --app app run`
