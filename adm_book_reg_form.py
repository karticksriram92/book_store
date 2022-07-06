from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, StopValidation, Optional
from wtforms import validators
import re

class Check_Length(object):
	def __init__(self, message=None):
		if not message:
			message = 'Must be 13 digit number.'
		self.message = message
	def __call__(self, form, field):
		if not re.search("^[0-9]{13}$", field.data):
			raise ValidationError(self.message)
			# ~ raise StopValidation(self.message)
		else:
			pass

class AddBook_Form(FlaskForm):
	name = StringField(label=("Name"), validators = [DataRequired(), Length(min=5, max=100)])
	author = StringField(label=("Author"), validators = [DataRequired(), Length(min=5, max=100)])
	publisher = StringField(label=("Publisher"), validators = [DataRequired(), Length(min=5, max=100)])
	price = IntegerField(label=("Price"), validators = [DataRequired(), NumberRange(min=0, max=1000)])
	description = TextAreaField(label=("Description"), validators = [DataRequired(), Length(min=300, max=3000)])
	isbn = StringField(label=("ISBN"), validators = [DataRequired(), Check_Length()])
	img = FileField(label=("Image"), validators = [FileRequired(), FileAllowed(['jpg', 'png'], 'Images only')])
	pdf = FileField(label=("Pdf"), validators = [FileRequired(), FileAllowed(['pdf'], 'Pdf only')])
	stock = IntegerField(label=("Stock"), validators = [DataRequired(), NumberRange(min=0, max=1000)])
	book_type = SelectField(label=("Book Type"), choices=[('fiction','Fiction'),('non-fiction','Non-Fiction'),('science', 'Science'),('biography','Biography')], validators= [DataRequired()])
	submit = SubmitField(label=("Add Book"))
