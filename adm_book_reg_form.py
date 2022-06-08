from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

# ~ def validate_isbn(form, field):
# ~ def check_isbn(form, field):
	# ~ print("hello")
	# ~ if not re.search("^[0-9]{13}$", field.data):
	# ~ if len(field.data)<13:
		# ~ print("hello")
		# ~ return ValidationError("Enter 13 digit length ISBN")

# ~ class Check_Length(object):
	# ~ def __init__(self, message=None):
		# ~ if not message:
			# ~ message = 'Field must be between 13 characters long.'
		# ~ self.message = message
	# ~ def __call__(self, form, field):
		# ~ if len(field.data)<13:
			# ~ raise ValidationError(self.message)
		# ~ else:
			# ~ print("hello")

class AddBook_Form(FlaskForm):
	name = StringField(label=("Name"), validators = [DataRequired(), Length(min=5, max=50)])
	author = StringField(label=("Author"), validators = [DataRequired(), Length(min=5, max=50)])
	publisher = StringField(label=("Publisher"), validators = [DataRequired(), Length(min=5, max=50)])
	price = IntegerField(label=("Price"), validators = [DataRequired(), NumberRange(min=0, max=1000)])
	description = TextAreaField(label=("Description"), validators = [DataRequired(), Length(min=50, max=1000)])
	isbn = IntegerField(label=("ISBN"), validators = [DataRequired()])
	img = FileField(label=("Image"), validators = [FileRequired(), FileAllowed(['jpg', 'png'], 'Images only')])
	pdf = FileField(label=("Pdf"), validators = [FileRequired(), FileAllowed(['pdf'], 'Pdf only')])
	stock = IntegerField(label=("Stock"), validators = [DataRequired(), NumberRange(min=0, max=1000)])
	submit = SubmitField(label=("Add Book"))

