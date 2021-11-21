from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL("online_store").query_db(query, data)
    @classmethod
    def edit(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s"
        return connectToMySQL("online_store").query_db(query, data)
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        result = connectToMySQL("online_store").query_db(query)
        return result
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL("online_store").query_db(query, data)
        return cls(result[0])
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL("online_store").query_db(query, data)
        return cls(result[0])
    @staticmethod
    def validate_user(user):
        valid = True
        if not len(user["first_name"]) > 1:
            flash("First name must be at least 2 characters")
            valid = False
        if not len(user["last_name"]) > 1:
            flash("Last name must be at least 2 characters")
            valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email")
            valid = False
        if not len(user["password"]) > 3:
            flash("Password must be at least 4 characters long")
            valid = False
        if not user["password"] == user["password_confirm"]:
            flash("Passwords do not match")
            valid = False
        return valid 
        