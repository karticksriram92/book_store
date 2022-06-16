from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_restful import Resource, Api
import sqlite3, uuid, stripe, json
from login import login_page, register_page
from home import home_page
from pdf import pdf_page
from search import search_page
from success import success_page
from view_book import view_book_page
from admin import adm_add_book_page, adm_view_book_page
from categorised_books import categorised_books_page
from book_form import BookForm


app = Flask(__name__, template_folder="templates")
api = Api(app)

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

@app.route("/cart", methods=["POST", "GET"])
def cart_page():
	form = BookForm()
	if form.validate_on_submit():
		cart_dict= { 'source' : 'view', 'book_id' : form.book_id.data, 'paperback': form.paperback.data, 'ebook' : form.ebook.data, 'no' : 1, 'status' : form.add_to_cart.data }
		if do_cart(card_dict):
			pass
	
	# ~ checkout_session_id=create_checkout_session(get_cart(session['uid'] if session['uid'] else ))
	return render_template('cart.html', checkout_session_id='', checkout_public_key=app.config['STRIPE_PUBLIC_KEY'])

# ~ #payment-stripe
stripe.api_key=app.config["STRIPE_SECRET_KEY"]

def create_checkout_session():
	checkout_session = stripe.checkout.Session.create(payment_method_types=['card'],line_items=[{
                    "name": "Learn Python",
                    "quantity": 1,
                    "currency": "inr",
                    "amount": "45000",
                },{
                    "name": "Learning SciPy",
                    "quantity": 1,
                    "currency": "inr",
                    "amount": "30000",
                },], mode='payment',success_url=request.host_url + 'success', cancel_url= request.host_url + 'cart',)
	return checkout_session

class get_session_id(Resource):
	def get(self):
		return "hi"
	def post(self):
		data = request.get_json()
		checkout_session = create_checkout_session()
		return jsonify(session_id=checkout_session['id'])

api.add_resource(get_session_id, '/get_sid')

############API#############
 
class get_username(Resource):
	def get(self):
		return "hello world"
	def post(self):
		data = request.get_json()
		username = get_uname(data['u_id'])
		return jsonify(username=username)
		
api.add_resource(get_username, "/get_u_id")

def get_uname(u_id_num):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select u_username from user where u_id=?",(u_id_num,))
	row = cursor.fetchone()
	return row[0]

class manage_cart(Resource):
	def get(self):
		return "hi"
	def post(self):
		if request.method == 'POST':
			data = request.get_json()
			if do_cart(data):
				return {}
			else:
				return "sorry", 500
	
api.add_resource(manage_cart, "/manage_cart")

def do_cart(cart_data):
	cart_dict = {}
	cart_dict_inner = {'paperback' : '', 'ebook' : '', 'no' : 0 }
	cart_dict_inner['paperback'] = cart_data['paperback']
	cart_dict_inner['ebook'] = cart_data['ebook']
	cart_dict_inner['no'] = cart_data['no']
	cart_dict[cart_data['book_id']] = cart_dict_inner
	if cart_data['source'] == 'cart':
		if update_cart(cart_dict, cart_data['book_id'], cart_data['status']):
			#must add code to get new checkout_session id with current cart details(get_cart).
			return True
	elif update_cart(cart_dict, cart_data['book_id'], cart_data['status']):
		return True
		
def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def get_cart(u_id):
	conn = sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	cursor.execute("select u_cart from user where u_id=?",(u_id,))
	rows = cursor.fetchall()
	conn.close()
	return rows[0]

def update_cart(cart_str=None, new_item, b_id, status):
	if 'uid' in session:
		cart_str = get_cart(session['uid'])
		tname = "user"
		uid = session['uid']
	if cart_str['u_cart']:
		cart_json = json.loads(cart_str['u_cart'])
		if b_id in cart_json.keys():
			if status == "added" or status == 'delete':
				cart_json.pop(b_id)
			elif status == 'update':
				cart_json[b_id]['paperback'] = new_item[b_id]['paperback']
				cart_json[b_id]['ebook'] = new_item[b_id]['ebook']
				cart_json[b_id]['no'] = new_item[b_id]['no']
			cdata = json.dumps(cart_json)
			print(cdata)
		else:
			cart_json[b_id] = new_item
			cdata = json.dumps(cart_json)
	else:
		cdata = json.dumps(new_item)
	return set_cart(cdata, uid, tname)
	
def set_cart(cart_data, uid, tname):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	query = "update {{0}} set u_cart=? where u_id=?".format(tname)
	data = cart_data, uid
	cursor.execute(query,(cdata, uid))
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()
		
