from flask import Flask, jsonify, request, render_template, redirect, url_for, session, make_response
from flask_restful import Resource, Api
from login import login_page, register_page, confirm_page, forgot_page, reset_page
from home import home_page
from pdf import pdf_page
from search import search_page
from success import success_page
from view_book import view_book_page
from admin import adm_add_book_page, adm_view_book_page
from categorised_books import categorised_books_page
from book_form import BookForm
import sqlite3, uuid, stripe, json, datetime


app = Flask(__name__, template_folder="templates")
api = Api(app)


app.config["SECRET_KEY"] = "test"
app.config["SECURITY_PASSWORD_SALT"] = "email-test"
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["STRIPE_PUBLIC_KEY"]="pk_test_51KzcRkSE3GG6tmtIKjMMMEQ5u1RrO6bc72VNQSsjktsWXyw4aXAt6Za8kEFEQIOJ9pXO1PYWkdbX5PPQFUYCozYW00wRXjLLz9"
app.config["STRIPE_SECRET_KEY"]="sk_test_51KzcRkSE3GG6tmtIDCHA8ybbSJgv8bTWeShIwnmsVrxP1BIavbzhnA2xt7GKNir7CzHWfQDK8d7ebQsABWtdklWJ00CXpyJJYL"

app.config.update(
	MAIL_SERVER = 'smtp.gmail.com',
	MAIL_PORT = 465,
	MAIL_USE_TLS = False,
	MAIL_USE_SSL = True,
	MAIL_USERNAME = 'sriram5130@gmail.com',
	MAIL_PASSWORD = 'tptfqmcnkytdzqbs'
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
		sum_data = updated_product(product_data, )
		if product_data:
			checkout_session = create_checkout_session(formatted_cart)
			products=True
		else:
			checkout_session={'id':''}
			products=False
	# ~ else:
		# ~ get_cart()
	# ~ checkout_session_id=create_checkout_session(get_cart(session['uid'] if session['uid'] else ))
	return render_template('cart.html', product_data=product_data, sum_data=sum_data, products=products, checkout_session_id=checkout_session['id'], checkout_public_key=app.config['STRIPE_PUBLIC_KEY'])

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
		data = request.get_json()
		if do_cart(data):
			if 'uid' in session:
				book_data, formatted_cart = format_cart(get_cart(session['uid']))
				updated_response = updated_product(book_data, b_id=data['book_id'])
				if data['status'] == 'delete':
					updated_response['status'] = data['status']
					updated_response = str(updated_response).replace("'", '"')
					return make_response(jsonify(updated_response), 200	)
				checkout_session = create_checkout_session(formatted_cart)
				updated_response['session_id'] = checkout_session['id']
				updated_response['status'] = data['status']
				updated_response = str(updated_response).replace("'", '"')
				return make_response(jsonify(updated_response), 200	)
		else:
			return "sorry", 500
	
api.add_resource(manage_cart, "/manage_cart")

class set_recent_views(Resource):
	def get(self):
		return ""
	def post(self):
		data = request.get_json()
		user_name = get_uname(data['u_id'])
		if user_name:
			if set_recent(data['book_id'], data['u_id']):
				return "", 200
			else:
				return "", 500
			
api.add_resource(set_recent_views, "/addRecent")

def set_recent(book_id, u_id):
	books = get_recent(book_id, u_id)
	time = str(datetime.datetime.now()).split('.')[0]
	if books:
		books = json.loads(books)
		if book_id in books.keys():
			books[book_id]['count'] = int(books[book_id]['count']) + 1
			books[book_id]['last_time'] = time
		else:
			b_name, b_img_small = get_name_img(book_id)
			books[book_id] = {'count' : 1 , 'name' : b_name, 'img' : b_img_small, 'last_time' : time }
		query="update recent_view set books=? where u_id=?"
	else:
		b_name, b_img_small = get_name_img(book_id)
		books = { book_id : { 'count' : 1, 'name' : b_name, 'img' : b_img_small, 'last_time' : time } }
		query="insert into recent_view(books, u_id) values(?,?)"
	books = json.dumps(books)
	data = (books, u_id)
	conn= sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute(query,data)
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True	
		
def get_name_img(book_id):
	conn= sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select b_name, b_img_small from book where b_id=?",(book_id,))
	row = cursor.fetchone()
	conn.close()
	if row:
		return row[0], row[1]
	
def get_recent(book_id, u_id):
	conn= sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	cursor.execute("select books from recent_view where u_id=?",(u_id,))
	row = cursor.fetchone()
	conn.close()
	if row:
		return row['books']

def updated_product(bdata, b_id=None):
	updated_dict = {}
	if len(bdata) == 0:
		updated_dict['book_id'] = b_id
		response_dict = calculatePayment(bdata, updated_dict)
		return response_dict
	for i in range(0,len(bdata)):
		if b_id in bdata[i]['b_id']:
			updated_dict['book_id'] = b_id
			updated_dict['paperback'] = str(bdata[i]['pbook_no'])
			updated_dict['ebook'] = str(bdata[i]['ebook_no'])
			updated_dict['ebook_total'] = str(bdata[i]['b_ebook_price'])
			updated_dict['pbook_total'] = str(bdata[i]['pbook_total'])
			response_dict = calculatePayment(bdata, updated_dict)
	if not b_id:
		updated_dict['ebook'] = str(bdata[i]['ebook_no'])
		updated_dict['ebook_total'] = str(bdata[i]['b_ebook_price'])
		updated_dict['pbook_total'] = str(bdata[i]['pbook_total'])
		response_dict = calculatePayment(bdata, updated_dict)
	return response_dict
			
def calculatePayment(bdata, udict):
	book_sum = 0
	total_sum = 0
	if len(bdata) == 0:
		udict['book_sum'] = 0.0
		udict['shipping'] = 0.0
		udict['total_sum'] = 0.0
		return udict
	for i in range(0, len(bdata)):
		if bdata[i]['ebook_no'] == 1:
			book_sum += bdata[i]['pbook_total'] + bdata[i]['b_ebook_price']
		else:
			book_sum += bdata[i]['pbook_total']
	udict['book_sum'] = str(book_sum)
	udict['shipping'] = 50
	udict['total_sum'] = str(book_sum+50)
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
			
	return book_details, product_list
	
def get_book_details(b_id):
	conn = sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	cursor.execute("select b_id, b_name, b_paperbook_price, b_ebook_price, b_img_small, b_stock from book where b_id=?",(b_id,))
	rows = cursor.fetchall()
	conn.close()
	return rows[0]



# ~ ########Mail#########
# ~ def send_mail(to, subject, template):
	# ~ msg = Message(subject=subject, sender="sriram5130@gmail.com", recipients=to)
	# ~ msg.html= template
	# ~ mail.send(msg)
	
# ~ @app.route('/email', methods=["POST", "GET"])
# ~ def handleRegister():
	# ~ if 'uid' in session:
		# ~ user_data=get_user_data(session['uid'])
		# ~ email = user_data['u_email']
	# ~ email=[]
	# ~ email.append(email_id)
	# ~ token = gen_conf_token(email)
	##url = request.base_url+'/confirm/'
	# ~ confirm_url = url_for('confirm_email', token=token)
	##confirm_url = url_for(url, token=token,  _extrenal=True)
	# ~ #must change splitting character based of url /e for /email
	# ~ confirm_url = request.base_url.split('/e')[0]+confirm_url
	# ~ html = render_template('activate.html', confirm_url=confirm_url)
	# ~ subject = "Please confirm your email"
	# ~ send_mail(email, subject, html)
	# ~ return "mail sent"
	
	# ~ #redirect to home page
	# ~ #saying confirmation mail is sent and user need to confirm.
	# ~ #(use flash or alert msg like navbar alert)
	
########Token#########
# ~ def gen_conf_token(email):
	# ~ serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
	# ~ return URLSafeTimedSerializer(email, salt=app.config['SECURITY_PASSWORD_SALT'])
	
# ~ def confirm_token(token, expiration=862000):
	# ~ serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
	# ~ try:
		# ~ email = serializer.loads(token, salt=app.config['SECRET_KEY'], max_age=expiration)
	# ~ except:
		# ~ return False
	# ~ else:
		# ~ return email
	
# ~ @app.route('/confirm/<token>')	
# ~ def confirm_email(token):
	# ~ try:
		# ~ email = confirm_token(token)
	# ~ except:
		# ~ print("the confirmation link is expired or failed")
		# ~ return "not working"
	# ~ #code for already confirmed goes here
	
	# ~ else:
		# ~ print("user confirmed")
		# ~ return "thanks for confirming"
		# ~ #confirm user and add to db of date time now and redirect
