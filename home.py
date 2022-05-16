from flask import Flask, request, render_template, redirect, url_for, Blueprint
from comment_form import Commentform
#kdkfjlkdfjkd

home_page = Blueprint("home_page", __name__, template_folder="templates")

@home_page.route("/home", methods=["POST","GET"])
def home():
	return render_template("home.html")
	#test
	# ~ return render_template("cart.html")
	# ~ form = Commentform()
	# ~ ratings_bar = [21, 32, 53, 67, 86]
	# ~ return render_template("view_book.html", form=form, bratings=ratings_bar)
