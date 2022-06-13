from flask import Flask, jsonify, request, render_template, redirect, url_for, session, Blueprint
from login_form import Loginform
from register_form import Registerform
from datetime import datetime
import sqlite3, uuid

login_page=Blueprint("login_page", __name__, template_folder="templates")

@login_page.route("/login", methods=["POST","GET"])
def login():
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
				return redirect("/")
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
