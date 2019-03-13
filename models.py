from flask_sqlalchemy import SQLAlchemy
from application import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    cash = db.Column(db.Integer, unique=False, nullable=False)
    userCurrent = db.relationship('userCurrent', backref='userC', lazy=True)
    userHistory = db.relationship('userHistory', backref='userH', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.cash}')"

class userCurrent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.String(250), unique=True, nullable=False)
    ppStock = db.Column(db.Integer, unique=False, nullable=False)
    netWorth = db.Column(db.Integer, unique=False, nullable=False)
    noShares = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"userCurrent('{self.stock}', '{self.ppStock}', '{self.netWorth}', '{self.noShares}')"

class userHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    historyStock = db.Column(db.String(250), unique=False, nullable=False)
    historyppStock = db.Column(db.Integer, unique=False, nullable=False)
    transType = db.Column(db.String(6), unique=False, nullable=False)
    transAmount = db.Column(db.Integer, unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))