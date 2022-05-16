from flask import Flask, request, render_template, redirect, url_for, Blueprint

search_page = Blueprint("search_page", __name__, template_folder="templates")

@search_page.route("/search", methods=["POST","GET"])
def doSearch():
	return render_template("search.html")
