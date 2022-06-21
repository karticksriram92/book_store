from flask import Flask, jsonify, request, render_template, redirect, url_for, session, Blueprint, current_app
from login_form import Loginform, ResetForm
from register_form import Registerform
from datetime import datetime
import sqlite3, uuid
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

#only inside blueprint it works. outside it makes an error
# ~ print(current_app.config['STRIPE_PUBLIC_KEY'])

login_page=Blueprint("login_page", __name__, template_folder="templates")

@login_page.route("/login", methods=["POST","GET"])
def login():
	print(current_app.config['STRIPE_PUBLIC_KEY'])
	# ~ print("hi")
	if 'uid' in session:
		return redirect("/")
	form = Loginform()
	msg=""
	if form.validate_on_submit():
		login_tuple=(form.username.data,form.password.data)
		user_id = check_login(login_tuple)
		if user_id:
			session["uid"] = user_id
			return redirect("/")
		msg="username or password is incorrect."
	return render_template("login.html", form=form, msg=msg)

def check_login(ldata):
	#this also works
	# ~ print(current_app.config['STRIPE_PUBLIC_KEY'])
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select u_id from user where u_username=? and u_password=?",ldata)
	result=cursor.fetchone()
	if result:
		conn.close()
		return result[0]
	conn.close()

register_page=Blueprint("register_page", __name__, template_folder="templates")

@register_page.route("/register", methods=["POST", "GET"])
def register():
	if 'uid' in session:
		return redirect("/")
	form = Registerform()
	msg={}
	if form.validate_on_submit():
		msg=check_username(form.username.data, form.email.data)
		print(msg)
		if not msg:
			if 'temp_id' in session:
				u_id = session['temp_id']
				cart = get_cart(session['temp_id'])
			else:
				u_id = get_id()
				cart = None
			signup_time = (datetime.now()).strftime("%d-%m-%Y %H:%M:%S")
			confirmed = "no"
			register_tuple=(u_id, form.fname.data, form.lname.data, form.username.data, form.email.data, None, form.password.data, cart, signup_time, confirmed)
			print(register_tuple)
			if do_register(register_tuple):
				session["uid"] = register_tuple[0]
				if handleRegister(form.email.data):
					return render_template('confirmation.html')
	return render_template("register.html", form=form, msg=msg)
	
def check_username(uname, email):
	status = {}
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select count(*) from user where u_username=?", (uname,))
	if(cursor.fetchone()[0]):
		status["username"]="Username exists already"
	cursor.execute("select count(*) from user where u_email=?", (email,))
	if(cursor.fetchone()[0]):
		status["email"]="Email exists already"
	conn.close()
	return status
	
def get_id():
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	while True:
		unique_u_id = str(uuid.uuid4())
		cursor.execute("select count(*) from user where u_id=?",(unique_u_id,))
		if not (cursor.fetchone()[0]):
			conn.close()
			return unique_u_id

def do_register(rdata):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("insert into user(u_id, u_first_name, u_last_name, u_username, u_email, u_address, u_password, u_cart, u_signup_time, u_confirmed) values(?,?,?,?,?,?,?,?,?,?)",rdata)
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()

########Mail#########
def send_mail(to, subject, template):
	mail = Mail(current_app)
	msg = Message(subject=subject, sender="BookStore", recipients=to)
	msg.html= template
	mail.send(msg)
	
def handleRegister(email_id):
	email=[]
	email.append(email_id)
	token = gen_conf_token(email)
	confirm_url = url_for('confirm_page.confirm_email', token=token, _external=True)
	html = render_template('activate.html', confirm_url=confirm_url)
	subject = "Please confirm your email"
	send_mail(email, subject, html)
	return True
	
def resendMail():
	if 'uid' in session:
		email = get_email(session['uid'])
		if handleRegister(email):
			return render_template('confirmation.html', resend=True)
			
########Token########
def gen_conf_token(email):
	serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
	return URLSafeTimedSerializer(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
	
def confirm_token(token, expiration=862000):
	serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
	try:
		email = serializer.loads(token, salt=current_app.config['SECRET_KEY'], max_age=expiration)
	except:
		return False
	else:
		return email
	
confirm_page=Blueprint("confirm_page", __name__, template_folder="templates")

@confirm_page.route("/confirm/<token>", methods=["POST","GET"])
def confirm_email(token):
	try:
		email = confirm_token(token)
	except:
		
		#includes resend mail option
		return render_template('confirmation_error.html')
	else:
		set_confirmation(email)
		return render_template('confirmation_success.html')
		
reset_page=Blueprint("reset_page", __name__, template_folder="templates")

@reset_page.route("/reset/<token>", methods=["POST","GET"])
def reset_email(token):
	try:
		email = confirm_token(token)
	except:
		#includes resend mail option
		return render_template('reset_error.html')
	else:
		form = resetForm()
		if form.validate_on_submit():
			if set_password(email, form.password.data):
				return render_template('reset_success.html')
		return render_template('reset_form.html', form=form)

def set_confirmation(email_id):
	status = {}
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select u_confirmed from user where u_email=?", (email_id,))
	row = cursor.fetchone()
	if row == "no":
		cursor.execute("update user set u_confirmed=? where u_email=?", ('yes', email_id))
		conn.commit()
		if(cursor.rowcount):
			conn.close()
			return True
	conn.close()

def set_password(email_id, password):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	reset_data = (email_id, password)
	cursor.execute("update user set u_password=? where u_email=?",reset_data)
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()

forgot_page=Blueprint('forgot_page', __name__, template_folder="templates")

@forgot_page.route('/forgot', methods=['POST','GET'])
def forgot():
	if request.method=="POST":
		email=request.form.get('email')
		if email_check(email):
			if set_reset(email):
				return render_template('reset_request.html')
	return render_template('forgot.html')

def set_reset(email_id):
	if handleReset(email_id):
		return True
	
def handleReset(email_id):
	email=[]
	email.append(email_id)
	token = gen_conf_token(email)
	confirm_url = url_for('confirm_page.confirm_email', token=token, _external=True)
	html = render_template('reset.html', confirm_url=confirm_url)
	subject = "Please confirm reset your password"
	send_mail(email, subject, html)
	return True

def email_check(email_id):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select count(*) from user where u_email=?", (email_id,))
	if(cursor.fetchone()[0]):
		conn.close()
		return True
	conn.close()
