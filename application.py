import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, get_flashed_messages, jsonify, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_session import Session
from flask_bcrypt import Bcrypt
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, lookup, usd



# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = "fbae185025fe828575acb367e5687f46"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


bcrypt= Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
db = SQLAlchemy(app)

from models import User, load_user
from forms import RegistrationForm, LoginForm, QuoteForm, BuyForm

db.create_all()


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


# Configure CS50 Library to use SQLite database


@app.route("/")
@app.route("/home")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    form = BuyForm()
    if form.validate_on_submit():
        buy_symbol = lookup(request.form.get("buy_symbol"))
        shares = request.form.get("shares")
        total = int(buy_symbol["latestPrice"]) * int(shares)
        if not buy_symbol:
            flash('Invalid Symbol', 'danger')
            return redirect("/buy")
        elif total > user.cash:
            flash('Not enough cash to complete transaction')
            return redirect("/buy")

    return render_template("buy.html", form=form)


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    if current_user.is_authenticated:
        return redirect("/")

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect("/")
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)




@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    logout_user()

    # Redirect user to login form
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quotes():
    """Get stock quote."""
    form = QuoteForm()
    if form.validate_on_submit() and request.method =="POST":
        quote_symbol = lookup(request.form.get("quote_symbol"))
        if not quote_symbol:
            flash('Invalid Symbol' + str(current_user.id), 'danger')
            return redirect("/quote")
        return render_template("quoted.html", stock=quote_symbol)
    else:
        return render_template("quote.html", form=form)






@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = hashed_password, cash = 10000)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for("login"))
    return render_template('register.html', title='Register', form=form)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
