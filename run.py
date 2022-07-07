from flask import Flask, request, render_template, redirect, url_for, session
from flask_restful import Api
from login import login_page, register_page, confirm_page, forgot_page, reset_page
from home import home_page
from pdf import pdf_page
from search import search_page
from success import success_page
from view_book import view_book_page
from admin import adm_add_book_page, adm_view_book_page, adm_update_book_page, adm_delete_book_page
from categorised_books import categorised_books_page
from cart import cart_page, get_username, get_session_id, manage_cart, set_recent_views
from book_form import BookForm
import sqlite3, uuid, os

app = Flask(__name__, template_folder="templates")
api = Api(app)

app.config["SECRET_KEY"] = "test"
app.config["SECURITY_PASSWORD_SALT"] = "email-test"
app.config["TEMPLATES_AUTO_RELOAD"] = True

# ~ app.config["STRIPE_PUBLIC_KEY"]= os.environ.get('STRIPE_PUB_KEY')
# ~ app.config["STRIPE_SECRET_KEY"]= os.environ.get('STRIPE_PVT_KEY')
app.config["STRIPE_PUBLIC_KEY"]= "pk_test_51KzcRkSE3GG6tmtIKjMMMEQ5u1RrO6bc72VNQSsjktsWXyw4aXAt6Za8kEFEQIOJ9pXO1PYWkdbX5PPQFUYCozYW00wRXjLLz9"
app.config["STRIPE_SECRET_KEY"]= "sk_test_51KzcRkSE3GG6tmtIDCHA8ybbSJgv8bTWeShIwnmsVrxP1BIavbzhnA2xt7GKNir7CzHWfQDK8d7ebQsABWtdklWJ00CXpyJJYL"

app.config.update(
	MAIL_SERVER = 'smtp.gmail.com',
	MAIL_PORT = 465,
	MAIL_USE_TLS = False,
	MAIL_USE_SSL = True,
	MAIL_USERNAME = 'sriram5130@gmail.com',
	MAIL_PASSWORD = 'tptfqmcnkytdzqbs'
	# ~ MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
	# ~ MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
)

app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.register_blueprint(confirm_page)
app.register_blueprint(forgot_page)
app.register_blueprint(reset_page)
app.register_blueprint(home_page)
app.register_blueprint(pdf_page)
app.register_blueprint(search_page)
app.register_blueprint(success_page)
app.register_blueprint(view_book_page)
app.register_blueprint(adm_add_book_page)
app.register_blueprint(adm_view_book_page)
app.register_blueprint(adm_update_book_page)
app.register_blueprint(adm_delete_book_page)
app.register_blueprint(categorised_books_page)
app.register_blueprint(cart_page)

api.add_resource(get_username, "/get_u_id")
api.add_resource(get_session_id, '/get_sid')
api.add_resource(manage_cart, "/manage_cart")
api.add_resource(set_recent_views, "/addRecent")

# ~ @app.before_request
# ~ def before_request():
	# ~ if request.endpoint != 'static/':
		# ~ 

@app.route("/")
def index():
	if session.get("uid"):
		return render_template("home.html")
	return redirect("/login")

@app.route("/logout")
def logout():
	session.pop("uid", None)
	return redirect(url_for("index"))
