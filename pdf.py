from flask import Flask, send_from_directory, Blueprint, render_template
import os

pdf_page = Blueprint('pdf_page', __name__, template_folder="templates")

@pdf_page.route('/pdf/<b_id>')
def showPdf(b_id):
	if check_book_owned(b_id):
		bpath = get_bookpath(b_id)
		workdir = os.path.abspath(os.getcwd())
		fpath = workdir + '/static/pdf/'
		return send_from_directory(fpath, bpath)
	# ~ return render_template('pdf.html')
	#send bad request

def check_book_owned(bid):
	if 'uid' in session:
		result= get_books_owned(session['uid'])
		if result:
			books_owned = result.split(',')
			if bid in books_owned:
				return True

def get_books_owned(uid):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select u_ebooks_owned from user where u_id=?",(u_id,))
	rows = cursor.fetchone()
	conn.close()
	return rows[0]

def get_bookpath(book_id):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select ub_pdf from book where u_id=?",(book_id,))
	rows = cursor.fetchone()
	conn.close()
	return rows[0]
