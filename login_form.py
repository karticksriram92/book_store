from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
#hkdkjhdjh

class Loginform(FlaskForm):
	username=StringField(label=("Username"), validators=[DataRequired()])
	password=PasswordField(label=("Password"), validators=[DataRequired()])
	submit=SubmitField(label=("Login"))
	
class ResetForm(FlaskForm):
	password=PasswordField(label=("Password"),validators=[DataRequired(), Length(min=8, max=30, message="")])
	cpassword=PasswordField(label=("Confirm Password"),validators=[DataRequired(), EqualTo('password')])
	submit=SubmitField(label=("Reset Password"))
