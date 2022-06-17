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
		if do_cart(cart_dict):
			pass
	
	if 'uid' in session:
		cart_details = get_cart(session['uid'])
		product_data, formatted_cart = format_cart(cart_details)
		
	# ~ else:
		# ~ get_cart()
	# ~ checkout_session_id=create_checkout_session(get_cart(session['uid'] if session['uid'] else ))
	return render_template('cart.html', product_data=product_data, checkout_session_id='', checkout_public_key=app.config['STRIPE_PUBLIC_KEY'])

# ~ #payment-stripe
stripe.api_key=app.config["STRIPE_SECRET_KEY"]

def create_checkout_session(total_items):
	checkout_session = stripe.checkout.Session.create(payment_method_types=['card'],line_items=total_items, mode='payment',success_url=request.host_url + 'success', cancel_url= request.host_url + 'cart',)
	return checkout_session

class get_session_id(Resource):
	def get(self):
		return "hi"
	def post(self):
		data = request.get_json()
		if 'uid' in session:
			book_data, formatted_cart = format_cart(get_cart(session['uid']))
			checkout_session = create_checkout_session(formatted_cart)
		# ~ else:
			# ~ checkout_session = create_checkout_session(format_cart(get_cart(session['uid']))
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
				print("data:")
				print(data)
				if 'uid' in session:
					book_data, formatted_cart = format_cart(get_cart(session['uid']))
					updated_response = updated_product(book_data, data['book_id'])
					checkout_session = create_checkout_session(formatted_cart)
					updated_response['session_id'] = checkout_session['id']
					print("all good till")
					updated_response = str(updated_response).replace("'", '"')
					print(updated_response)
					return json.dumps(updated_response), 200	
			else:
				return "sorry", 500
	
api.add_resource(manage_cart, "/manage_cart")

def updated_product(bdata, b_id):
	updated_dict = {}
	for i in range(0,len(bdata)):
		if b_id in bdata[i]['b_id']:
			updated_dict['book_id'] = b_id
			updated_dict['paperback'] = bdata[i]['pbook_no']
			updated_dict['ebook'] = bdata[i]['ebook_no']
			updated_dict['pbook_total'] = bdata[i]['pbook_total']
			response_dict = calculatePayment(bdata, updated_dict)
	return response_dict
			
def calculatePayment(bdata, udict):
	book_sum = 0
	total_sum = 0
	for i in range(0, len(bdata)):
		if bdata[i]['ebook_no'] == 1:
			book_sum += bdata[i]['pbook_total'] + bdata[i]['b_ebook_price']
		else:
			book_sum += bdata[i]['pbook_total']
	udict['book_sum'] = book_sum
	udict['shipping'] = 50
	udict['total_sum'] = book_sum+50
	return udict
		

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

def update_cart(new_item, b_id, status, cart_str=None):
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
		else:
			cart_json[b_id] = new_item[b_id]
			cdata = json.dumps(cart_json)
	else:
		cdata = json.dumps(new_item)
	return set_cart(cdata, uid, tname)
	
def set_cart(cart_data, uid, tname):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	query = "update {0} set u_cart=? where u_id=?".format(tname)
	data = (cart_data, uid)
	cursor.execute(query,data)
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()
		
def format_cart(cdetails):
	book_details = []
	product_list = []
	cdetails = json.loads(cdetails['u_cart'])
	for bid in cdetails.keys():
		book_details.append(get_book_details(bid))
		
	#return book_details also with product_list
	for i in range(0,len(book_details)):
		if cdetails[book_details[i]['b_id']]['paperback'] == 'no' and cdetails[book_details[i]['b_id']]['no'] == 1:
			product_list.append({ "name" : book_details[i]['b_name']+"(ebook)", "quantity" :  1, "currency" : "inr", "amount" : str(int(book_details[i]['b_ebook_price'])*int(cdetails[book_details[i]['b_id']]['no']))+"00" })
			book_details[i]['pbook_no'] = 0
			book_details[i]['ebook_no'] = 1
			book_details[i]['pbook_total'] = 0
		elif cdetails[book_details[i]['b_id']]['ebook'] == 'no':
			product_list.append({ "name" : book_details[i]['b_name']+"(paperbook)", "quantity" :  cdetails[book_details[i]['b_id']]['no'], "currency" : "inr", "amount" : str(int(book_details[i]['b_paperbook_price'])*int(cdetails[book_details[i]['b_id']]['no']))+"00" })
			book_details[i]['pbook_no'] = int(cdetails[book_details[i]['b_id']]['no'])
			book_details[i]['ebook_no'] = 0
			book_details[i]['pbook_total'] = float(int(cdetails[book_details[i]['b_id']]['no']) * int(book_details[i]['b_paperbook_price']))
		else:
			product_list.append({ "name" : book_details[i]['b_name']+"(paperbook)", "quantity" :  cdetails[book_details[i]['b_id']]['no'], "currency" : "inr", "amount" : str(int(book_details[i]['b_paperbook_price'])*int(cdetails[book_details[i]['b_id']]['no']))+"00" })
			product_list.append({ "name" : book_details[i]['b_name']+"(ebook)", "quantity" :  1, "currency" : "inr", "amount" : str(int(book_details[i]['b_ebook_price'])*int(cdetails[book_details[i]['b_id']]['no']))+"00" })
			book_details[i]['pbook_no'] = int(cdetails[book_details[i]['b_id']]['no'])
			book_details[i]['ebook_no'] = 1
			book_details[i]['pbook_total'] = float(int(cdetails[book_details[i]['b_id']]['no']) * int(book_details[i]['b_paperbook_price']))
			
	print("book_details")
	print(book_details)
	return book_details, product_list
	
def get_book_details(b_id):
	conn = sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	cursor.execute("select b_id, b_name, b_paperbook_price, b_ebook_price, b_img_small, b_stock from book where b_id=?",(b_id,))
	rows = cursor.fetchall()
	conn.close()
	return rows[0]
