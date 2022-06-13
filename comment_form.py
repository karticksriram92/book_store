from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, ValidationError

class Commentform(FlaskForm):
	name=StringField(label=("Name"), validators=[DataRequired(), Length(min=5, max=30)])
	email=StringField(label=("Email"), validators=[DataRequired(), Email()])
	comment=TextAreaField(label=("Review"), validators=[DataRequired(), Length(min=10, max=1000)])
	rstar=HiddenField('rstar')
	submit_review=SubmitField(label=("Post Review"))
