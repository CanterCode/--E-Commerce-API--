from flask import Blueprint, request, jsonify
from main import db, User, Product, Order, user_schema, users_schema, product_schema, products_schema, order_schema, orders_schema
from marshmallow import ValidationError
from sqlalchemy import select

routes = Blueprint('routes', __name__)

# =====================================
#              USERS
# =====================================

# Get all users
@routes.route('/users', methods=['GET'])
def get_users():
    users = db.session.execute(select(User)).scalars().all()
    return users_schema.jsonify(users), 200

# Get a single user by ID
@routes.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    return user_schema.jsonify(user), 200

# Create a new user
@routes.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_user = User(**user_data)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

# Update an existing user
@routes.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User, id)
    for key, value in request.json.items():
        setattr(user, key, value)
    db.session.commit()
    return user_schema.jsonify(user), 200

# Delete a user
@routes.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

# =====================================
#            PRODUCTS
# =====================================

# Get all products
@routes.route('/products', methods=['GET'])
def get_products():
    products = db.session.execute(select(Product)).scalars().all()
    return products_schema.jsonify(products), 200

# Get a single product by ID
@routes.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.get(Product, id)
    return product_schema.jsonify(product), 200

# Create a new product
@routes.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_product = Product(**product_data)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product), 201

# Update an existing product
@routes.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = db.session.get(Product, id)
    for key, value in request.json.items():
        setattr(product, key, value)
    db.session.commit()
    return product_schema.jsonify(product), 200

# Delete a product
@routes.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.get(Product, id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200


# =====================================
#             ORDERS
# =====================================

# Create a new order
@routes.route('/orders', methods=['POST'])
def create_order():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_order = Order(**order_data)
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order), 201

# Add a product to an order
@routes.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
def add_product_to_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)
    if product not in order.products:
        order.products.append(product)
        db.session.commit()
    return order_schema.jsonify(order), 200

# Remove a product from an order (product_id in request body)
@routes.route('/orders/<int:order_id>/remove_product', methods=['DELETE'])
def remove_product_from_order(order_id):
    product_id = request.json.get('product_id')
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)
    if product in order.products:
        order.products.remove(product)
        db.session.commit()
    return jsonify({"message": "Product removed from order"}), 200

# Get all orders for a specific user
@routes.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    orders = db.session.execute(select(Order).where(Order.user_id == user_id)).scalars().all()
    return orders_schema.jsonify(orders), 200

# Get all products in a specific order
@routes.route('/orders/<int:order_id>/products', methods=['GET'])
def get_products_in_order(order_id):
    order = db.session.get(Order, order_id)
    return products_schema.jsonify(order.products), 200