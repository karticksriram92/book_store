import os, random, uuid, sqlite3, base64
from io import BytesIO

# ~ def get_img_path(img_data):
	# ~ unique_fname = str(uuid.uuid4())
	# ~ fname = os.path.join(os.path.dirname(app.app.instance_path), 'static/images', unique_fname+'.jpg')
	# ~ img_data.save(fname)
	# ~ return fname

# ~ def save_img(img_data):
	# ~ img=Image.open(BytesIO(img_data))
	# ~ return get_img_path(img)
	
def migration_prep(srow):
	temp_list=[]
	for i in range(len(srow[0])):
		if i==4:
			ebook_price = float(int(srow[0][4]-((srow[0][4]/100)*30)))
			temp_list.append(srow[0][4])
			temp_list.append(ebook_price)
			continue
		temp_list.append(srow[0][i])
	return tuple(temp_list)

def get_book(b_id_num):
	conn = sqlite3.connect("./database/book_store.db")
	cursor = conn.cursor()
	cursor.execute("select * from book where b_id=?",(b_id_num,))
	row = cursor.fetchall()
	return row

def do_add_book(book_data):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("insert into book(b_id, b_name, b_author, b_publisher, b_paperbook_price, b_ebook_price, b_desc, b_isbn, b_type, b_img, b_img_small, b_pdf, b_stock) values(?,?,?,?,?,?,?,?,?,?,?,?,?)", book_data)
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()

def get_books_id():
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select * from books")
	# ~ cursor.execute("select * from book")
	rows = cursor.fetchall()
	for row in rows:
		print("processing id: "+str(row[0]))
		# ~ if do_add_book(migration_prep(get_book(row[0]))):
		# ~ if change_id(row):
		if migrate_book(row):
		# ~ if change_table(row)
			print("id processed: "+str(row[0]))
		else:
			print("failed: "+str(row[0]))

def migrate_book(b_data):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("insert into book(b_id, b_name, b_author, b_publisher, b_paperbook_price, b_ebook_price, b_desc, b_isbn , b_type, b_img, b_img_small, b_pdf, b_stock, b_avg_rating, b_total_rating) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", b_data)
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()

def change_id(book_data):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("update review set b_id=? where b_id=? ", book_data)
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()
	
def check_id():
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	while True:
		unique_id = str(uuid.uuid4())
		cursor.execute("select count(*) from book_mig where new_b_id=?",(unique_id,))
		if not (cursor.fetchone()[0]):
			return unique_id

# ~ get_books_id()
