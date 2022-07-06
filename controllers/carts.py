from itertools import count
from unicodedata import name
from flask_app import app
from flask import render_template, redirect, flash, request, session
from flask_app.models.cart import Cart
from flask_app.models.user import User

@app.route('/cart')
def cart():
    print(session["user_id"])
    print(session["cart_id"])
    total =  0
    data = {
        "total": total,
        "user_id": session["user_id"],
        "cart_id": session["cart_id"]
    }
    prices = Cart.get_all_prices_by_id(data)
    for price in prices:
        total += price["price"]
    Cart.update_total(data)
    cart = Cart.get_products_by_id(data)
    print(cart[0])
    temp = {}
    temp[cart[0].get('name')] = 1
    for product in cart:
        a = product.get('name')
        if a not in temp:
            temp[a] = 1
        else:
            temp[a] = temp[a] + 1
    print(temp.keys())
    return render_template("cart.html", cart = cart, total = total, temp = temp)
@app.route('/new')
def new():
    data = {
        "id": session["user_id"],
        "total": 0
    }
    Cart.new_cart(data)
    ids = Cart.get_ids()
    print(ids)
    current_id = 1
    for id in ids:
        if(id["id"] > current_id):
            current_id = id["id"]
    session["cart_id"] = current_id
    return redirect('/dashboard')