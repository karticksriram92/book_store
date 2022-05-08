from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class Registerform(FlaskForm):
	username=StringField(label=("Username"), validators=[DataRequired(), Length(min=8, max=30)])
	password=PasswordField(label=("Password"), validators=[DataRequired(), Length(min=8, max=30, message="")])
	cpassword=PasswordField(label=("Confirm Password"), validators=[DataRequired(), EqualTo('password')])
	fname=StringField(label=("First Name"), validators=[DataRequired()])
	lname=StringField(label=("Last Name"), validators=[DataRequired()])
	email=StringField(label=("Email"), validators=[DataRequired(), Email()])
	address=TextAreaField(label=("Address"), validators=[DataRequired(), Length(min=20, max=100)])
	submit=SubmitField(label=("Register"))
