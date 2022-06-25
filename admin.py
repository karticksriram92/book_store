from flask import Flask, request, render_template, redirect, url_for, session, Blueprint, current_app
from adm_book_reg_form import AddBook_Form
import sqlite3, random, uuid, io, os
from PIL import Image

adm_view_book_page = Blueprint("adm_view_book_page", __name__, template_folder="templates")
adm_add_book_page = Blueprint("adm_add_book_page", __name__, template_folder="templates")
adm_update_book_page = Blueprint("adm_update_book_page", __name__, template_folder="templates")

@adm_view_book_page.route('/admin/view_book', methods=['POST','GET'])
def view_book():
	books_data = get_books()
	print(books_data)
	return render_template('adm_view_book.html', books_data=books_data)
	
def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d
	
def get_books():
	conn = sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor= conn.cursor()
	cursor.execute("select * from book")
	rows=cursor.fetchall()
	return rows

@adm_add_book_page.route('/admin/add_book', methods=['POST', 'GET'])
def add_book():
	print(current_app.config['STRIPE_PUBLIC_KEY'])
	print("hi")
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
			print(book_tuple)
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
	resized_img = img.resize(sizes)
	return get_img_path(resized_img)
	# ~ img_bytes_arr= io.BytesIO()
	# ~ new_img.save(img_bytes_arr, format="JPEG")
	# ~ return img_bytes_arr.getvalue()
	
@adm_update_book_page.route('/admin/update_book/<bid>', methods=['POST','GET'])
def update_book(bid):
	form=AddBook_Form()
	book_data = get_book_data(bid)
	form.name.data = book_data['b_name']
	form.author.data = book_data['b_author']
	form.publisher.data = book_data['b_publisher']
	form.price.data = book_data['b_paperbook_price']
	form.description.data = book_data['b_desc']
	form.isbn.data = book_data['b_isbn']
	form.book_type.data = book_data['b_type']
	form.stock.data = book_data['b_stock']
	return render_template('adm_update_book.html', form=form)
	
def get_book_data(b_id):
	conn = sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor= conn.cursor()
	cursor.execute("select * from book where b_id=?", (b_id,))
	row=cursor.fetchone()
	return row
	
def get_img_path(img_data):
	unique_fname = str(uuid.uuid4())
	fname = os.path.join(os.path.dirname(app.app.instance_path), 'static/', unique_fname+'.jpg')
	img_data.save(fname)
	return fname
	
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
	fname = os.path.join(os.path.dirname(app.app.instance_path), 'static/', unique_fname+'.pdf')
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
