from flask import Flask, request, render_template, redirect, url_for, Blueprint, session, current_app
import sqlite3, json

home_page = Blueprint("home_page", __name__, template_folder="templates")

@home_page.route("/", methods=["POST","GET"])
def home():
	trending_book = get_books('trending_book',7)
	new_arrival = get_books('new_arrival',7)
	if 'uid' in session:
		recent_view = get_recent_views(session['uid'],  7)
		print(recent_view)
	else:
		recent_view=""
		# ~ recent_view = get_recent_views(session['uid'],  7, order='date')
	return render_template("home.html", trending_book=trending_book, new_arrival=new_arrival, recent_view=recent_view)

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def get_books(tname, part, uid=None):
	conn = sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	sql_query="select * from {0}".format(tname)
	cursor.execute(sql_query)
	rows = cursor.fetchall()
	if rows:
		parted_rows=[rows[i:i+part] for i in range(0, len(rows), part)]
		return parted_rows

def get_recent_views(uid, part):
	conn = sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	cursor.execute("select books from recent_view where u_id=?",(uid,))
	rows = cursor.fetchall()
	if rows:
		rows=rows[0]['books']
		format_recent_views(json.loads(rows),part)
	
def format_recent_views(rv_data, part):
	frview = []
	temp_dict = {}
	for item in rv_data.keys():
		temp_dict['b_id'] = item
		temp_dict['b_name'] = rv_data[item]['name']
		temp_dict['count'] = rv_data[item]['count']
		temp_dict['last_time'] = rv_data[item]['last_time']
		temp_dict['b_img_small'] = rv_data[item]['img']
		frview.append(temp_dict)
		print(frview)
	if len(frview)<7:
		part=len(frview)
	parted_rows=[frview[i:i+part] for i in range(0, len(frview), part)]
	print(parted_rows)
	return parted_rows
		
# ~ def order_set(frv):
	# ~ for i in frv:
		# ~ if 
	
