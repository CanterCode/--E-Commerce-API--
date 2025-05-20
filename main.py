from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, Table, Column, String, Integer, Float, DateTime
from datetime import datetime
from marshmallow import ValidationError
from typing import List, Optional
from __future__ import annotations

# Initialize Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:JMC100@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating our Base Model
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

# Association Table
order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", ForeignKey("order_id"), primary_key=True),
    Column("product_id", ForeignKey("product_id"), primary_key=True)
)

# User model
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    # One-to-Many: One user can have many orders
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")


# Order model
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Many-to-One: Belongs to one user
    user: Mapped["User"] = relationship("User", back_populates="orders")

    # Many-to-Many: Order has multiple products
    products: Mapped[List["Product"]] = relationship("Product", secondary=order_product, back_populates="orders")


# Product model
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # Many-to-Many: Product is in multiple orders
    orders: Mapped[List["Order"]] = relationship("Order", secondary=order_product, back_populates="products")
    
    
#======= Schemas =======#

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True
        load_instance = True

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


#======= Routes =======#

@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_user = User(
        name=user_data['name'],
        address=user_data['address'],
        email=user_data['email']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.jsonify(new_user), 201