from flask_app.models.product import Product
from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, flash
class Cart:
    def __init__(self, data):
        self.total = data["total"],
        self.user_id = data["id"]
    @classmethod
    def get_carts_by_id(cls, data):
        query = "SELECT * FROM cart WHERE user_id = %(id)s"
        result = connectToMySQL("online_store").query_db(query, data)
        return result
    @classmethod
    def get_products_by_id(cls, data):
        query = "SELECT * FROM cart LEFT JOIN products ON products.cart_id = cart.id WHERE products.cart_id = %(cart_id)s"
        results = connectToMySQL("online_store").query_db(query, data)
        return results
    @classmethod
    def get_all_prices_by_id(cls, data):
        query = "SELECT price FROM cart LEFT JOIN products ON products.cart_id = cart.id WHERE products.cart_id = %(cart_id)s"
        results = connectToMySQL("online_store").query_db(query, data)
        return results
    @classmethod
    def update_total(cls, data):
        query = "UPDATE cart SET total = %(total)s WHERE id = %(cart_id)s"
        return connectToMySQL("online_store").query_db(query, data)
    @classmethod
    def get_ids(cls):
        query = "SELECT id FROM cart"
        result = connectToMySQL("online_store").query_db(query)
        return result
    @classmethod
    def new_cart(cls, data):
        query = "INSERT INTO cart (total, user_id) VALUES (%(total)s, %(id)s)"
        return connectToMySQL("online_store").query_db(query, data)


