from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_restful import Resource, Api
import sqlite3, uuid
from login import login_page, register_page

app = Flask(__name__, template_folder="templates")
#api = Api(app)
app.config["SECRET_KEY"] = "hello"
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.register_blueprint(login_page)
app.register_blueprint(register_page)

@app.route("/")
def index():
	if not session.get("uid"):
		return redirect("/login")
	return render_template("index.html")

@app.route("/logout")
def logout():
	session.pop("uid", None)
	return redirect(url_for("index"))

# ~ class Test(Resource):
	# ~ def get(self):
		# ~ return jsonify({'name':'kartick'})
		
# ~ api.add_resource(Test, "/")
