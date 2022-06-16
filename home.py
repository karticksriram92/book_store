from flask import Flask, request, render_template, redirect, url_for, Blueprint
import sqlite3

home_page = Blueprint("home_page", __name__, template_folder="templates")

@home_page.route("/home", methods=["POST","GET"])
def home():
	trending_book = get_books('trending_book',7)
	print(trending_book)
	new_arrival = get_books('new_arrival',7)
	recent_view = get_books('recent_view',7)
	return render_template("home.html", trending_book=trending_book, new_arrival=new_arrival, recent_view=recent_view)

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def get_books(tname, part):
	conn = sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	sql_query="select * from {0}".format(tname)
	cursor.execute(sql_query)
	rows = cursor.fetchall()
	if rows:
		parted_rows=[rows[i:i+part] for i in range(0, len(rows), part)]
		return parted_rows
