from flask import Flask, request, render_template, redirect, url_for, session, Blueprint, current_app
from adm_book_reg_form import AddBook_Form
import sqlite3, random, uuid, io, os
from PIL import Image

adm_view_book_page = Blueprint("adm_view_book_page", __name__, template_folder="templates")
adm_add_book_page = Blueprint("adm_add_book_page", __name__, template_folder="templates")
adm_update_book_page = Blueprint("adm_update_book_page", __name__, template_folder="templates")
adm_delete_book_page = Blueprint("adm_delete_book_page", __name__, template_folder="templates")

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
			ebook_price = float(form.price.data)-((float(form.price.data)/100)*30)
			book_tuple=(book_id, form.name.data, form.author.data, form.publisher.data, float(form.price.data), ebook_price, form.description.data, form.isbn.data, form.book_type.data, full_img, small_img, pdf_path, form.stock.data)
			print("prepped")
			print(book_tuple)
			if do_add_book(book_tuple):
				form=AddBook_Form(formdata=None)
				return render_template('adm_add_book.html', form=form)
	else:
		print("not working")
		pass
	return render_template('adm_add_book.html', form=form, msg=msg)

@adm_delete_book_page.route('/admin/delete_book/<bid>', methods=['POST','GET'])
def delete_book(bid):
    if do_delete_book(bid):
        return redirect('/admin/view_book')

@adm_update_book_page.route('/admin/update_book/<bid>', methods=['POST','GET'])
def update_book(bid):
	book_data = get_book_data(bid)
	msg=''
	options = ['fiction','non-fiction','science','biography']
	if request.method == 'POST':
		if not request.form.get('isbn') == book_data['b_isbn']:
			msg = check_isbn(request.form.get('isbn'))
		if not msg:
			if not request.form.get('img'):
				full_img = book_data['b_img']
				small_img = book_data['b_img_small']
			else:
				full_img = resize_img(request.form.get('img'))
				small_img = resize_img(request.form.get('img'), small=True)
			if not request.form.get('pdf'):
				pdf_path = book_data['b_pdf']
			else:
				pdf_path= get_pdf_path(request.form.get('pdf'))
			ebook_price = float(request.form.get('price'))-((float(request.form.get('price'))/100)*30)
			book_tuple=(request.form.get('name'), request.form.get('author'), request.form.get('publisher'), float(request.form.get('price')), ebook_price, request.form.get('description'), request.form.get('isbn'), request.form.get('book_type'), full_img, small_img, pdf_path, request.form.get('stock'), bid)
			print(book_tuple)
			if do_update_book(book_tuple):
				book_data = get_book_data(bid)
				for i in range(0,len(options)):
					if options[i] == book_data['b_type']:
						rec = i
				return render_template('adm_update_book.html', book_data=book_data, rec=rec)
		else:
			print(book_tuple)
			return render_template('adm_update_book.html', book_data='', msg=msg)
	# ~ img = open(os.path.join(os.path.dirname(current_app.instance_path), 'static'+book_data['b_img']), 'rb')
	# ~ pdf = open(os.path.join(os.path.dirname(current_app.instance_path), 'static'+book_data['b_pdf']), 'rb')
	for i in range(0,len(options)):
		if options[i] == book_data['b_type']:
			rec = i
	return render_template('adm_update_book.html', book_data=book_data, rec=rec, msg=msg)
	
def get_book_data(b_id):
	conn = sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor= conn.cursor()
	cursor.execute("select * from book where b_id=?", (b_id,))
	row=cursor.fetchone()
	return row

def resize_img(img, small=False):
	sizes = (150,250) if small else (250,350)
	#trying open method with bytesIO
	img = Image.open(img.stream)
	resized_img = img.resize(sizes)
	return get_img_path(resized_img)
		
def get_img_path(img_data):
	unique_fname = str(uuid.uuid4())
	fname = os.path.join(os.path.dirname(app.app.instance_path), 'static/', unique_fname+'.jpg')
	img_data.save(fname)
	return fname
	
def get_id():
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	while True:
		unique_b_id = str(uuid.uuid4())
		cursor.execute("select count(*) from book where b_id=?",(unique_b_id,))
		if not (cursor.fetchone()[0]):
			conn.close()
			return unique_b_id

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
	cursor.execute("insert into book(b_id, b_name, b_author, b_publisher, b_paperbook_price, b_ebook_price, b_desc, b_isbn, b_type, b_img, b_img_small, b_pdf, b_stock) values(?,?,?,?,?,?,?,?,?,?,?,?)", book_data)
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()

def do_update_book(book_data):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("update book set b_name=?, b_author=?, b_publisher=?, b_paperbook_price=?, b_ebook_price=?, b_desc=?, b_isbn=?, b_type=?, b_img=?, b_img_small=?, b_pdf=?, b_stock=? where b_id=?", book_data)
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()

def do_delete_book(book_id):
    conn = sqlite3.connect("./database/bookstore.db")
    cursor = conn.cursor()
    cursor.execute("delete from book where b_id=?", (book_id,))
    conn.commit()
    if(cursor.rowcount):
        conn.close()
        return True
    conn.close()
