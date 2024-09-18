import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from flask_cors import CORS

app = Flask(__name__)
ma = Marshmallow(app)
CORS(app)

class CustomerSchema(ma.Schema):
    id = fields.String(required=False)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)
    class Meta:
        fields = ('id', 'name', 'email', 'phone')

class ProductSchema(ma.Schema):
    id = fields.Integer(required= False)
    product_name = fields.String(required= True)
    price = fields.Float(required= True)
    product_details = fields.String()
    class Meta:
        fields = ('id', 'product_name', 'price', 'product_details')

class OrderSchema(ma.Schema):
    id = fields.Integer(required= False)
    order_date_ = fields.Date(required= True)
    customer_id = fields.Integer(required= True)
    product_id = fields.Integer(required=True)
    class Meta:
        fields = ('id', 'order_date', 'customer_id', 'product_id')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many = True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many= True)

product_schema = ProductSchema()
products_schema = ProductSchema(many= True)

# postgresql://postgresql_ecomm_148_user:9aIbqpdK7zjj4kUbfkECEBnqh9duXu5f@dpg-crl1v3t6l47c73fq6b5g-a/postgresql_ecomm_148

db_name = "postgresql_ecomm_148"
user = "postgresql_ecomm_148_user"
password = "9aIbqpdK7zjj4kUbfkECEBnqh9duXu5f"
host = "dpg-crl1v3t6l47c73fq6b5g-a"

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )

        if conn.is_connected():
            print("Connected successfully")
            return conn

    except Error as e:
        print(f"Error: {e}")
        return None

# Customer Table:
@app.route('/customers', methods = ['GET'])
def get_customers():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM Customers"
        cursor.execute(query)
        customers = cursor.fetchall()
        return customers_schema.jsonify(customers)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    try: 
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        customer_to_get = (id, )
        cursor.execute("SELECT * FROM Customers WHERE id = %s", customer_to_get)
        customer = cursor.fetchall()
        return customers_schema.jsonify(customer)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        new_customer = (customer_data['name'], customer_data['email'], customer_data['phone'])
        query = "INSERT INTO Customers (name, email, phone) VALUES (%s, %s, %s)"
        cursor.execute(query, new_customer)
        conn.commit()
        return jsonify({"message": "New customer added successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    try:
        customer_info = customer_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        updated_customer = (customer_info['name'], customer_info['email'], customer_info['phone'], id)
        query = "UPDATE Customers SET name = %s, email = %s, phone = %s WHERE id = %s"
        cursor.execute(query, updated_customer)
        conn.commit()
        return jsonify({"message": "Customer info updated successfully"}), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        customer_to_remove = (id, )
        cursor.execute("SELECT * FROM Customers WHERE id = %s", customer_to_remove)
        customer = cursor.fetchone()
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        
        query = "DELETE FROM Customers WHERE id = %s"
        cursor.execute(query, customer_to_remove)
        conn.commit()
        return jsonify({"message": "Customer removed successfully"}), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Products Table:
@app.route("/products", methods= ['GET'])
def get_product_list():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM products"
        cursor.execute(query)
        products = cursor.fetchall()
        return products_schema.jsonify(products)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/products/<int:id>", methods= ['GET'])
def get_product(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        product_to_get = (id, )
        cursor.execute("SELECT * FROM products WHERE id =%s", product_to_get)
        product = cursor.fetchall()
        return products_schema.jsonify(product)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/products', methods=['POST'])
def add_product():
    try:
        product_info = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
    
        new_product = (product_info['product_name'], product_info['price'], product_info['product_details'])
        query= "INSERT INTO products (product_name, price, product_details) VALUES (%s, %s, %s)"
        cursor.execute(query, new_product)
        conn.commit()

        return jsonify({"message": "New product added successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/products/<int:id>', methods=['PUT'])
def update_product_info(id):
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_product = (product_data['product_name'], product_data['price'], product_data['product_details'])
        query= "UPDATE customers SET product_name = %s, price = %s, product_details = %s WHERE id = %s"
        cursor.execute(query, new_product)
        conn.commit()
        return jsonify({"message": "Product details updated successfully"}), 200
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/products/<int:id>', methods=['DELETE'])
def remove_product(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()
        product_to_remove = (id, )
        cursor.execute("SELECT * FROM products WHERE id = %s", product_to_remove)
        product = cursor.fetchone()
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        query = "DELETE FROM products WHERE id = %s"
        cursor.execute(query, product_to_remove)
        conn.commit()
        return jsonify({"message": "Customer removed successfully"}), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Orders Table:
@app.route("/orders", methods=['GET'])
def retrieve_orders():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM orders"
        cursor.execute(query)
        orders = cursor.fetchall()
        return orders_schema.jsonify(orders)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/orders/<int:order_id>", methods= ['GET'])
def get_order(order_id):
    breakpoint()
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)
        order_to_get = (order_id, )
        cursor.execute("SELECT * FROM orders WHERE id =%s", order_to_get)
        order = cursor.fetchall()
        return orders_schema.jsonify(order)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/orders', methods=['POST'])
def add_order():
    try:
        order_info = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        new_order = (order_info['order_date'], order_info['customer_id'], order_info['product_id'])
        query = "INSERT INTO orders (order_date, customer_id, product_id) VALUES (%s, %s, %s)"
        cursor.execute(query, new_order)
        conn.commit()
        return jsonify({"message": "New order added"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    try:
        order_info = order_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400

    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        updated_order = (order_info['order_date'], order_info['customer_id'], order_info['product_id'], id)
        query = "UPDATE ORDERS SET order_date = %s, customer_id = %s, product_id = %s WHERE id = %s"
        cursor.execute(query, updated_order)
        conn.commit()
        return jsonify({"message": "Order info updated successfully"}), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        order_to_remove = (id, )
        cursor.execute("SELECT * FROM orders WHERE id = %s", order_to_remove)
        order = cursor.fetchone()
        if not order:
            return jsonify({"error": "Order not found"}), 404
        query = "DELETE FROM orders WHERE id = %s"
        cursor.execute(query, order_to_remove)
        conn.commit()
        return jsonify({"message": "Order removed successfully"}), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)