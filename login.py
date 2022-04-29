from flask import Flask, jsonify, request, render_template, redirect, url_for, session, Blueprint

home_page=Blueprint("home_page", __name__, template_folder="templates")


@home_page.route("/")
def index():
	# ~ if not session.get("uid"):
		# ~ return redirect(url_for("login"))
	return render_template("index.html")
