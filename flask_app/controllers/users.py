from logging import NullHandler
from flask_app import app
from flask import render_template, redirect, flash, request, session
from flask_app.models.user import User
from flask_app.models.cart import Cart
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template("login.html")
@app.route('/login', methods= ["POST"])
def login():
    user = User.get_user_by_email(request.form)
    if not user:
        flash("Invalid email")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid password")
        return redirect('/')
    session["user_id"] = user.id
    ids = Cart.get_ids()
    current_id = 1
    for id in ids:
        if(id["id"] > current_id):
            current_id = id["id"]
    session["cart_id"] = current_id
    return redirect('/dashboard')
@app.route('/register')
def create():
    return render_template("create.html")
@app.route("/new_user", methods= ["POST"])
def new_user():
    if not User.validate_user(request.form):
        return redirect('/register')
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"], 
        "password": pw_hash
    }
    User.save(data)
    session["user_id"] = User.get_user_by_email(data).id
    return redirect('/dashboard')
@app.route('/dashboard')
def dashboard():
    data = {
        "id": session["user_id"]
    }
    user = User.get_user_by_id(data)
    return render_template("dashboard.html", user = user)
@app.route('/account')
def account():
    return render_template("account.html")
@app.route('/edit', methods= ["POST"])
def edit():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "password_confirm": request.form["password"]
    }
    if not User.validate_user(data):
        return redirect('/account')
    User.edit(request.form)
    return redirect('/account')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')