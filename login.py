from flask import Flask, jsonify, request, render_template, redirect, url_for, session, Blueprint
import sqlite3

login_page=Blueprint("login_page", __name__, template_folder="templates")

@login_page.route("/login")
def login():
	return render_template("login.html")
	
check_page=Blueprint("check_page", __name__, template_folder="templates")

@check_page.route("/login_check", methods=["POST"])
def login_check():
	result = request.form.to_dict()
	login_data = (result["username"], result["password"])
	lstatus = check_login(login_data)
	if lstatus:
		session["uid"] = result["username"]
	return redirect(url_for("index"))

def check_login(ldata):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select count(*) from login where name=? and password=?",ldata)
	if(cursor.fetchone()[0]):
		conn.close()
		return True
	conn.close()
