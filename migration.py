from PIL import Image
import app
import os, random, uuid, sqlite3, base64
from io import BytesIO

def get_img_path(img_data):
	unique_fname = str(uuid.uuid4())
	fname = os.path.join(os.path.dirname(app.app.instance_path), 'static/images', unique_fname+'.jpg')
	img_data.save(fname)
	return fname

def save_img(img_data):
	img=Image.open(BytesIO(img_data))
	return get_img_path(img)

def get_book(b_id_num):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select * from book where b_id=?",(b_id_num,))
	row = cursor.fetchall()
	row=list(row[0])
	row[8]=save_img(row[8])
	row[9]=save_img(row[9])
	return row

def do_add_book(book_data):
	conn = sqlite3.connect("./database/book_store.db")
	cursor = conn.cursor()
	cursor.execute("insert into book(b_id, b_name, b_author, b_publisher, b_price, b_desc, b_isbn, b_type, b_img, b_img_small, b_pdf, b_stock) values(?,?,?,?,?,?,?,?,?,?,?,?)", book_data)
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()

def get_books_id():
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select b_id from book")
	rows = cursor.fetchall()
	for row in rows:
		print("processing id: "+str(row[0]))
		if do_add_book(get_book(row[0])):
			print("id processed: "+str(row[0]))
		else:
			print("failed: "+str(row[0]))

get_books_id()
