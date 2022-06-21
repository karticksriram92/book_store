from flask import Flask, request, render_template, redirect, url_for, Blueprint

success_page = Blueprint("success_page", __name__, template_folder="templates")

@success_page.route("/success", methods=["POST"])
def doSuccess():
	# ~ updateStock()
	# ~ updateUser()
	# ~ clearCart()
	return render_template("success.html")

# ~ def updateStock():
	
