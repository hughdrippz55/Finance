from flask_sqlalchemy import SQLAlchemy
from application import db, login_manager
from flask_login import UserMixin
import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    cash = db.Column(db.Integer, unique=False, nullable=False)
    userCurrent = db.relationship('userCurrent', backref='userC', lazy=True, uselist=False)
    userHistory = db.relationship('userHistory', backref='userH', lazy=True, uselist=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.cash}')"

class userCurrent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=False, nullable=False)
    symbolName = db.Column(db.String(300), unique=False, nullable=False)
    ppStock = db.Column(db.Integer, unique=False, nullable=False)
    netWorth = db.Column(db.Integer, unique=False, nullable=True)
    noShares = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    userH = db.relationship(User)

    @property
    def serialize(self):
        if self.noShares == 1:
            selectOption = f'{self.symbolName} - ({self.noShares} share) - ${self.ppStock}/share'
        else:
            selectOption = f'{self.symbolName} - ({self.noShares} shares) - ${self.ppStock}/share'
        return f"{self.symbol}, {self.noShares}", selectOption

    def __repr__(self):
        return f"{self.symbol}, {self.noShares}"

class userHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    historySymbol = db.Column(db.String(10), unique=False, nullable=False)
    historySymbolName = db.Column(db.String(300), unique=False, nullable=False)
    noSharesHistory = db.Column(db.Integer, unique=False, nullable=False)
    historyppStock = db.Column(db.Integer, unique=False, nullable=False)
    transType = db.Column(db.String(6), unique=False, nullable=False)
    transAmount = db.Column(db.Integer, unique=False, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    userC = db.relationship


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))