from __future__ import annotations
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, Table, Column, String, Integer, Float, DateTime
from datetime import datetime
from marshmallow import ValidationError
from typing import List, Optional
from routes import routes
from models import db, ma, User, Product, Order, user_schema, users_schema, product_schema, products_schema, order_schema, orders_schema


# Initialize Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:JMC100@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Marshmallow
db.init_app(app)
ma.init_app(app)

app.register_blueprint(routes)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    print("🚀 Starting Flask server...")  # <-- Add this print to verify it's running
    app.run(debug=True)