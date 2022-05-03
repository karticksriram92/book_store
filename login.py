from flask import Flask, jsonify, request, render_template, redirect, url_for, session, Blueprint
from login_form import Loginform
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

@register_page.route("/register")
def register():
	return render_template("register.html")
	
register_check = Blueprint("register_check", __name__, template_folder="templates")
	
@register_check.route("/register_check")
def check_register():
	result = request.form.to_dict()
	login_data = (result["username"], result["password"], result["address"])
	rstatus = do_register(register_data)
	if rstatus:
		session["uid"] = result["username"]
	return redirect(url_for("index"))
	
def do_register(rdata):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select count(*) from login where name=? and password=?",ldata)
	if(cursor.fetchone()[0]):
		conn.close()
		return True
	conn.close()
