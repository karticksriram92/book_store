from flask import Flask, Blueprint, render_template, redirect
import sqlite3

categorised_books_page = Blueprint('categorised_books_page', __name__,template_folder='templates')

@categorised_books_page.route('/books_category/<b_category>', methods=['POST','GET'])
def categorised__books(b_category):
	search_results=get_search_results(b_category)
	if search_results:
		books_data=get_books(search_results, 4)
		return render_template('categorised_books.html', books_data=books_data, category=b_category)
	return redirect('/home')
	
def get_search_results(squery):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select b_id from book where b_type=?",(squery,))
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

