from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError
#hkdkjhdjh

class Loginform(FlaskForm):
	username=StringField(label=("Username"), validators=[DataRequired()])
	password=PasswordField(label=("Password"), validators=[DataRequired()])
	submit=SubmitField(label=("Login"))
	
