from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField

class BookForm(FlaskForm):
	book_id = HiddenField("book_id")
	paperback = HiddenField("paperback")
	ebook = HiddenField("ebook")
	add_to_cart = HiddenField("add_to_cart")
	submit_buy = SubmitField(label=("Buy Book"))
