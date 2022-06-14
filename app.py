from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_restful import Resource, Api
import sqlite3, uuid, stripe
from login import login_page, register_page
from home import home_page
from pdf import pdf_page
from search import search_page
from success import success_page
from view_book import view_book_page
from admin import adm_add_book_page, adm_view_book_page
from categorised_books import categorised_books_page



# ~ app = Flask(__name__, template_folder="templates")
app = Flask('app', template_folder="templates")

app.config["SECRET_KEY"] = "test"
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["STRIPE_PUBLIC_KEY"]="pk_test_51KzcRkSE3GG6tmtIKjMMMEQ5u1RrO6bc72VNQSsjktsWXyw4aXAt6Za8kEFEQIOJ9pXO1PYWkdbX5PPQFUYCozYW00wRXjLLz9"
app.config["STRIPE_SECRET_KEY"]="sk_test_51KzcRkSE3GG6tmtIDCHA8ybbSJgv8bTWeShIwnmsVrxP1BIavbzhnA2xt7GKNir7CzHWfQDK8d7ebQsABWtdklWJ00CXpyJJYL"

app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.register_blueprint(home_page)
app.register_blueprint(pdf_page)
app.register_blueprint(search_page)
app.register_blueprint(success_page)
app.register_blueprint(view_book_page)
app.register_blueprint(adm_add_book_page)
app.register_blueprint(adm_view_book_page)
app.register_blueprint(categorised_books_page)

@app.route("/")
def index():
	if session.get("uid"):
		return render_template("home.html")
	return redirect("/login")

@app.route("/logout")
def logout():
	session.pop("uid", None)
	return redirect(url_for("index"))

# ~ #payment-stripe
stripe.api_key=app.config["STRIPE_SECRET_KEY"]

@app.route("/cart", methods=["POST", "GET"])
def create_checkout_session():
	# ~ form.validate_on_submit():
	
	#already commented out version. dont uncomment it.
	# ~ checkout_session = stripe.checkout.Session.create(payment_method_types=['card'],line_items=[{'price_data' : {'currency' : 'inr','unit_amount' : 500,'product_data' : {'name' : 'name of the product',},},'quantity' : 1,},], mode='payment',success_url=my_domain + '/success.html', cancel_url=my_domain + '/cancel.html',)

	checkout_session = stripe.checkout.Session.create(payment_method_types=['card'],line_items=[{
                    "name": "Learn Python",
                    "quantity": 1,
                    "currency": "inr",
                    "amount": "25000",
                },{
                    "name": "Learning SciPy",
                    "quantity": 1,
                    "currency": "inr",
                    "amount": "30000",
                },], mode='payment',success_url=request.host_url + 'success', cancel_url= request.host_url + 'cart',)
	
	return render_template('cart.html', checkout_session_id=checkout_session['id'], checkout_public_key=app.config['STRIPE_PUBLIC_KEY'])
