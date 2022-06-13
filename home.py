from flask import Flask, request, render_template, redirect, url_for, Blueprint

home_page = Blueprint("home_page", __name__, template_folder="templates")

@home_page.route("/home", methods=["POST","GET"])
def home():
	return render_template("home.html")
