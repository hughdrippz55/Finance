from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, AnyOf
from FinanceApp.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=16)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError("Username unavailable. Please choose another")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class QuoteForm(FlaskForm):

    quote_symbol = StringField('Symbol', validators=[DataRequired(), Length(min = 1)])
    submit = SubmitField('Get Quote')

class BuyForm(FlaskForm):

    buy_symbol = StringField("Stock Symbol", validators=[DataRequired()])
    shares = IntegerField("Amount of Shares", validators=[DataRequired(message='Invalid input. Enter a number above zero only')])
    submit = SubmitField('Buy Stock')


class SellForm(FlaskForm):
    stocks = SelectField('Select stock to sell', validators=[DataRequired()])
    amountToSell = IntegerField('Amount of Shares', validators=[DataRequired()])
    sell = SubmitField('Sell Stock')