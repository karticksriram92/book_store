from flask import Flask, jsonify, request, render_template, redirect, url_for, session, Blueprint
from login_form import Loginform
from register_form import Registerform
import sqlite3

login_page=Blueprint("login_page", __name__, template_folder="templates")

@login_page.route("/login", methods=["POST","GET"])
def login():
	form = Loginform()
	msg=""
	if form.validate_on_submit():
		login_tuple=(form.username.data,form.password.data)
		if login_check(login_tuple):
			return redirect("/")
		msg="username or password is incorrect."
	return render_template("login.html", form=form, msg=msg)

def login_check(login_data):
	print(login_data)
	lstatus = check_login(login_data)
	if lstatus:
		session["uid"] = login_data[0]
		return True

def check_login(ldata):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select count(*) from login where name=? and password=?",ldata)
	if(cursor.fetchone()[0]):
		conn.close()
		return True
	conn.close()

register_page=Blueprint("register_page", __name__, template_folder="templates")

@register_page.route("/register", methods=["POST", "GET"])
def register():
	form = Registerform()
	msg={}
	if form.validate_on_submit():
		msg=check_username(form.username.data, form.email.data)
		print(msg)
		if not msg:
			register_tuple=(form.username.data, form.password.data, form.fname.data, form.lname.data, form.email.data, form.address.data)
			print(register_tuple)
			if do_register(register_tuple):
				session["uid"] = register_tuple[0]
				return redirect("/")
	return render_template("register.html", form=form, msg=msg)
	
def check_username(uname, email):
	status = {}
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select count(*) from user where username=?", (uname,))
	if(cursor.fetchone()[0]):
		status["username"]="Username exists already"
	cursor.execute("select count(*) from user where email=?", (email,))
	if(cursor.fetchone()[0]):
		status["email"]="Email exists already"
	conn.close()
	return status
	
def do_register(rdata):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("insert into user(username, password, first_name, last_name, email, address) values(?,?,?,?,?,?)",rdata)
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()
