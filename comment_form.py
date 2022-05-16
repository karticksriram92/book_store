from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

class Commentform(FlaskForm):
	name=StringField(label=("Your Name"), validators=[DataRequired(), Length(min=8, max=30)])
	email=StringField(label=("Your Email"), validators=[DataRequired(), Email()])
	comment=TextAreaField(label=("Your Comment"), validators=[DataRequired(), Length(min=10, max=300)])
	submit=SubmitField(label=("Post Comment"))
