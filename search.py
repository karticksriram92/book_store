from flask import Flask, request, render_template, redirect, url_for, Blueprint
import sqlite3, re, base64

search_page = Blueprint("search_page", __name__, template_folder="templates")

#had to remove get from methods after implementing
@search_page.route("/search", methods=["POST","GET"])
def doSearch():
	if request.method == "POST":
		print("post received")
		search_query = request.form.get("search")
		print(search_query)
		search_results = get_search_results(search_query)
		if search_results:
			books_data = get_books(search_results,4)
			return render_template("search.html",search_query=search_query, books_data=books_data)
	return redirect('/home')

def regtest(value, pattern):
	pattern_str=pattern
	if len(pattern.split())>1:
		pattern_str=pattern+'|'+'|'.join(pattern.split())
	compiled_pattern=re.compile(r'^(.*?('+pattern_str.lower()+r').*)$', re.MULTILINE)
	return compiled_pattern.search(value.lower()) is not None

def get_search_results(squery):
	conn = sqlite3.connect("./database/bookstore.db")
	conn.create_function("regtest", 2, regtest)
	cursor = conn.cursor()
	cursor.execute("select b_id from book where regtest(b_name, ?)",(squery,))
	rows = cursor.fetchall()
	results = []
	for row in rows:
		results.append(row[0])
	conn.close()
	return results
	
def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def get_books(b_id_list, part):
	conn = sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	sql_query="select * from book where b_id in ({0})".format(', '.join('?'*len(b_id_list)))
	cursor.execute(sql_query, b_id_list)
	rows = cursor.fetchall()
	parted_rows=[rows[i:i+part] for i in range(0, len(rows), part)]
	return parted_rows
