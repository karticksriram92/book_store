from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_restful import Resource, Api
import sqlite3, uuid
from login import home_page

app = Flask(__name__, template_folder="templates")
#api = Api(app)
app.config["SECRET_KEY"] = "hello"
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.register_blueprint(home_page)

# ~ @app.route("/login")
# ~ def login():
	# ~ return render_template("login.html")

# ~ @app.route("/login_check", methods=["POST"])
# ~ def login_check():
	# ~ result = request.form.to_dict()
	# ~ login_data = (result["username"], result["password"])
	# ~ lstatus = check_login(login_data)
	# ~ if lstatus:
		# ~ session["uid"] = result["username"]
	# ~ return redirect(url_for("index"))

# ~ def check_login(ldata):
	# ~ conn = sqlite3.connect("./database/bookstore.db")
	# ~ cursor = conn.cursor()
	# ~ cursor.execute("select count(*) from login where name=? and password=?",ldata)
	# ~ if(cursor.fetchone()[0]):
		# ~ conn.close()
		# ~ return True
	# ~ conn.close()

# ~ @app.route("/logout")
# ~ def logout():
	# ~ session.pop("uid", None)
	# ~ return redirect(url_for("index"))

# ~ class Test(Resource):
	# ~ def get(self):
		# ~ return jsonify({'name':'kartick'})
		
# ~ api.add_resource(Test, "/")
