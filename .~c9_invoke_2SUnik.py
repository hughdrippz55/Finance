import os
import datetime
import re
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, get_flashed_messages, jsonify, redirect, render_template, session, request, url_for
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
now = datetime.datetime.now()

from models import User, load_user, userCurrent, userHistory
from forms import RegistrationForm, LoginForm, QuoteForm, BuyForm, SellForm

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
        buy_symbol = lookup(str(request.form.get("buy_symbol")))
        if buy_symbol:
            company_name = buy_symbol["name"]
            symbol_name = buy_symbol["symbol"]
            symbol_price = float(buy_symbol["price"])
            shares = int(form.shares.data)
            if shares > 0:
                total = float(symbol_price * shares)
                user = User.query.filter_by(id = current_user.id).first()
                symbol_check = userCurrent.query.filter_by(user_id = current_user.id, symbol = symbol_name).first()
                if user.cash < total:
                    flash("Not enough cash in account to complete transaction", "danger")
                    return redirect("/buy")
                elif symbol_check:
                    user.cash -= total
                    symbol_check.noShares += shares
                    user_history = userHistory(historySymbol = symbol_name, historySymbolName = company_name, noSharesHistory = shares, historyppStock = symbol_price, transType = "Buy", transAmount = total, user_id = current_user.id)
                    db.session.add(user_history)
                    db.session.commit()
                    if shares == 1:
                        flash(f"You have successfully purchased {shares} share of {symbol_name}", "success")
                        return redirect("/buy")
                    else:
                        flash(f"You have successfully purchased {shares} shares of {symbol_name}", "success")
                        return redirect("/buy")
                    return redirect("/buy")
                else:
                    user.cash -= total
                    user_current = userCurrent(symbol = symbol_name, symbolName = company_name, ppStock = symbol_price, noShares = shares, user_id = current_user.id)
                    user_history = userHistory(historySymbol = symbol_name, historySymbolName = company_name, noSharesHistory = shares, historyppStock = symbol_price, transType = "Buy", transAmount = total, user_id = current_user.id)
                    db.session.add(user_current)
                    db.session.add(user_history)
                    db.session.commit()
                    flash(f"You have successfully purchased {shares} shares of {company_name}", "success")
                    return redirect("/buy")
            else:
                flash("Invalid input. Enter a number above zero only", "danger")
        else:
            flash("Invalid Symbol", "danger")
    return render_template("buy.html", form=form)
        # if not buy_symbol:
        #     flash('Invalid Symbol', 'danger')
        #     return redirect("/buy")
        # elif total > user.cash:
        #     flash('Not enough cash to complete transaction')
        #     return redirect("/buy")


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
        stock = [(userCurrent.symbol_name, userCurrent.noShares) for item in userCurrent.query.filter_by(user_id = current_user.id, symbol = symbol_name).order_all()]
    """Sell shares of stock"""
    options = userCurrent.query.filter_by(user_id = current_user.id).order_by(userCurrent.symbolName).all()
    stockOpt = [row.serialize for row in options]
    form = SellForm(stocks='Select a Stock')
    form.stocks.choices = stockOpt
    return render_template("sell.html", form=form)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
