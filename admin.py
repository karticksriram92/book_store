from flask import Flask, request, render_template, redirect, url_for, session, Blueprint
from adm_book_reg_form import AddBook_Form
import sqlite3, random, uuid
from PIL import Image
import app
import io
import os


view_book_page = Blueprint("view_book_page", __name__, template_folder="templates")
add_book_page = Blueprint("add_book_page", __name__, template_folder="templates")

@view_book_page.route('/admin/view_book', methods=['POST','GET'])
def view_book():
	return render_template('adm_view_book.html')

@add_book_page.route('/admin/add_book', methods=['POST', 'GET'])
def add_book():
	form=AddBook_Form()
	msg=""
	if form.validate_on_submit():
		print("form validating")
		msg = check_isbn(form.isbn.data)
		if not msg:
			print("msg empty")
			book_id = get_id()
			full_img = resize_img(form.img.data)
			small_img = resize_img(form.img.data, small=True)
			pdf_path= get_pdf_path(form.pdf.data)
			book_tuple=(book_id, form.name.data, form.author.data, form.publisher.data, form.price.data, form.description.data, form.isbn.data, form.book_type.data, full_img, small_img, pdf_path, form.stock.data)
			print("prepped")
			if do_add_book(book_tuple):
				form=AddBook_Form(formdata=None)
				return render_template('adm_add_book.html', form=form)
	else:
		print("not working")
		pass
	return render_template('adm_add_book.html', form=form, msg=msg)

def resize_img(img, small=False):
	sizes = (150,250) if small else (250,350)
	#trying open method with bytesIO
	img = Image.open(img.stream)
	
	new_img = img.resize(sizes)
	qval = 80
	img_bytes_arr= io.BytesIO()
	new_img.save(img_bytes_arr, format="JPEG")
	return img_bytes_arr.getvalue()
	
def get_id():
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	while True:
		rand_id = random.randrange(100000, 999999)
		cursor.execute("select count(*) from book where b_id=?",(rand_id,))
		if not (cursor.fetchone()[0]):
			conn.close()
			return rand_id

def check_isbn(isbn_num):
	print("checking isbn")
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select count(*) from book where b_isbn=?",(isbn_num,))
	if(cursor.fetchone()[0]):
		conn.close()
		status = "This isbn/book exists already"
		return status

def get_pdf_path(pdf_data):
	unique_fname = str(uuid.uuid4())
	fname = os.path.join(os.path.dirname(app.app.instance_path), 'static/pdf', unique_fname+'.pdf')
	print(fname)
	pdf_data.save(fname)
	return fname
	
def do_add_book(book_data):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("insert into book(b_id, b_name, b_author, b_publisher, b_price, b_desc, b_isbn, b_type, b_img, b_img_small, b_pdf, b_stock) values(?,?,?,?,?,?,?,?,?,?,?,?)", book_data)
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()
