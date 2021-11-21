from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.product import Product
from flask_app.models.cart import Cart
from flask_app.models.user import User

@app.route('/products')
def products():
    products = Product.get_all()
    return render_template("products.html", products = products)
@app.route('/add_to_cart/<int:inventory_id>')
def add_to_cart(inventory_id):
    data = {
        "id": session["user_id"] 
    }
    if not Cart.get_carts_by_id(data):
        data = {
            "total": 0,
            "user_id": session["user_id"]
        }
        Cart.new_cart(data)
        ids = Cart.get_ids()
        print(ids)
        current_id = 1
        for id in ids:
            if(id["id"] > current_id):
                current_id = id["id"]
        session["cart_id"] = current_id
    data = {
        "inventory_id": inventory_id
    }
    product = Product.get_inventory_by_id(data)[0]
    if not Product.validate(product):
        return redirect('/products')
    update = product["quantity"] - 1
    
    data = {
        "name": product["name"],
        "description": product["description"],
        "quantity": update,
        "price": product["price"],
        "inventory_id": product["inventory_id"],
        "cart_id": session["cart_id"]
    }
    Product.update_inventory(data)
    Product.add_to_cart(data)
    
    return redirect('/products')
@app.route('/add/<int:product_id>')
def add(product_id):
    data = {
        "product_id": product_id
    }

    product = Product.get_product_by_id(data)[0]
    data = {
        "name": product["name"]
    }
    inventory = Product.get_inventory_by_name(data)[0]
    if not Product.validate(inventory):
        return redirect('/cart')
    update = inventory["quantity"] - 1
    data = {
        "quantity": update,
        "inventory_id": inventory["inventory_id"],
        "product_id": product_id
    }
    Product.update_inventory(data)
    Product.add_to_cart(product)
    return redirect('/cart')
@app.route('/remove/<int:product_id>')
def remove(product_id):
    data = {
        "product_id": product_id
    }
    product = Product.get_product_by_id(data)[0]
    data = {
        "name": product["name"]
    }
    inventory = Product.get_inventory_by_name(data)[0]
    update = inventory["quantity"] + 1
    data = {
        "quantity": update,
        "inventory_id": inventory["inventory_id"],
        "product_id": product_id
    }
    Product.update_inventory(data)
    Product.remove(data)
    return redirect('/cart')
