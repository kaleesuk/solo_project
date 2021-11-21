from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
class Product:
    def __init__(self, data):
        self.inventory_id = data["id"]
        self.name = data["name"]
        self.quantity = data["quantity"]
        self.price = data["price"]
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM inventory"
        result = connectToMySQL("online_store").query_db(query)
        return result
    @classmethod
    def get_inventory_by_id(cls, data):
        query = "SELECT * FROM inventory WHERE inventory_id = %(inventory_id)s"
        result = connectToMySQL("online_store").query_db(query, data)
        return result
    @classmethod
    def get_inventory_by_name(cls, data):
        query = "SELECT * FROM inventory WHERE name = %(name)s"
        result = connectToMySQL("online_store").query_db(query, data)
        return result
    @classmethod
    def get_product_by_id(cls, data):
        query = "SELECT * FROM products WHERE product_id = %(product_id)s"
        result = connectToMySQL("online_store").query_db(query, data)
        return result
    @classmethod
    def update_inventory(cls, data):
        query = "UPDATE inventory SET quantity = %(quantity)s WHERE inventory_id = %(inventory_id)s"
        return connectToMySQL("online_store").query_db(query, data)
    @classmethod 
    def add_to_cart(cls, data):
        query = "INSERT INTO products (name, price, cart_id) VALUES (%(name)s, %(price)s, %(cart_id)s)"
        return connectToMySQL("online_store").query_db(query, data)
    @classmethod
    def remove(cls, data):
        query = "DELETE FROM products WHERE product_id = %(product_id)s"
        return connectToMySQL("online_store").query_db(query, data)
    @staticmethod
    def validate(product):
        valid = True
        if not product["quantity"] > 0:
            flash("Insufficient amount in stock")
            valid = False
        return valid
