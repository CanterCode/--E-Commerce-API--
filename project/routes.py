from flask import Blueprint, request, jsonify
from models import db, User, Product, Order, user_schema, users_schema, product_schema, products_schema, order_schema, orders_schema
from marshmallow import ValidationError
from sqlalchemy import select

routes = Blueprint('routes', __name__)

# =====================================
#              USERS
# =====================================

# GET all users
@routes.route('/users', methods=['GET'])
def get_users():
    users = db.session.execute(select(User)).scalars().all()
    return users_schema.jsonify(users), 200

# GET a single user by ID
@routes.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return user_schema.jsonify(user), 200

# CREATE a new user
@routes.route('/users', methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(user_data)
    db.session.commit()
    return user_schema.jsonify(user_data), 201

# UPDATE a user by ID
@routes.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    for key, value in request.json.items():
        setattr(user, key, value)
    db.session.commit()
    return user_schema.jsonify(user), 200

# DELETE a user by ID
@routes.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

# =====================================
#            PRODUCTS
# =====================================

# GET all products
@routes.route('/products', methods=['GET'])
def get_products():
    products = db.session.execute(select(Product)).scalars().all()
    return products_schema.jsonify(products), 200

# GET a single product by ID
@routes.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return product_schema.jsonify(product), 200

# CREATE a new product
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

# UPDATE a product by ID
@routes.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    for key, value in request.json.items():
        setattr(product, key, value)
    db.session.commit()
    return product_schema.jsonify(product), 200

# DELETE a product by ID
@routes.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200

# =====================================
#             ORDERS
# =====================================

# CREATE a new order
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

# ADD a product to an existing order
@routes.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
def add_product_to_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)

    if not order or not product:
        return jsonify({"error": "Order or Product not found"}), 404

    if product not in order.products:
        order.products.append(product)
        db.session.commit()
    return order_schema.jsonify(order), 200

# REMOVE a product from an order (requires product_id in JSON body)
@routes.route('/orders/<int:order_id>/remove_product', methods=['DELETE'])
def remove_product_from_order(order_id):
    product_id = request.json.get('product_id')
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)

    if not order or not product:
        return jsonify({"error": "Order or Product not found"}), 404

    if product in order.products:
        order.products.remove(product)
        db.session.commit()
    return jsonify({"message": "Product removed from order"}), 200

# GET all orders placed by a specific user
@routes.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    orders = db.session.execute(select(Order).where(Order.user_id == user_id)).scalars().all()
    return orders_schema.jsonify(orders), 200

# GET all products in a specific order
@routes.route('/orders/<int:order_id>/products', methods=['GET'])
def get_products_in_order(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return products_schema.jsonify(order.products), 200