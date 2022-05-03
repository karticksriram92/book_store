from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#hhh

class Loginform(FlaskForm):
	username=StringField(label=("Username"), validators=[DataRequired(), Length(min=8, max=30, message="Must be between 8 to 30 characters.")]
	password=PasswordField(label=("Password"), validators=[DataRequired(), Length(min=8, max=30, message="Must be atleast 8 to 30 characters long.")])
	submit=SubmitField(label=("Login"))
	
