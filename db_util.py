import sqlite3

# ~ create_query="create table user(username varchar(30) primary key , password varchar(30), first_name varchar(30), last_name varchar(30), email varchar(30), address varchar(100))"
# ~ create_query="create table user(username varchar(30) primary key , password varchar(30), first_name varchar(30), last_name varchar(30), email varchar(30), address varchar(100))"
# ~ select_query="select * from user"
# ~ drop_query="drop table user"
# ~ select_count_query="select count(*) from login where name=? and password=?"
# ~ insert_query="insert into login(name, password) values('karticksriram','sriram20')"
# ~ delete_query="delete from user where username=?"
# ~ delete_username=("karticksriram",)

# ~ def insert_login(query):
	# ~ conn = sqlite3.connect("./database/bookstore.db")
	# ~ cursor = conn.cursor()
	# ~ cursor.execute(query)
	# ~ conn.commit()
	# ~ if cursor.rowcount:
		# ~ print(cursor.rowcount)
	# ~ conn.close()
	
# ~ def select_login(query):
	# ~ conn = sqlite3.connect("./database/bookstore.db")
	# ~ cursor = conn.cursor()
	# ~ cursor.execute(query)
	# ~ data = cursor.fetchall()
	# ~ for row in data:
		# ~ print(row)
	# ~ conn.close()
	
# ~ data=('karticksriram','sriram20')

# ~ def select_count_login(query,ldata):
	# ~ conn = sqlite3.connect("./database/bookstore.db")
	# ~ cursor = conn.cursor()
	# ~ cursor.execute(query,ldata)
	# ~ print(cursor.fetchone()[0])
	# ~ conn.close()

# ~ #select_count_login_db(select_count_query,data)


# ~ def create_table(query):
	# ~ conn = sqlite3.connect("./database/bookstore.db")
	# ~ cursor = conn.cursor()
	# ~ cursor.execute(query)
	# ~ print("tabel created")
	# ~ conn.close()

# ~ def delete_table(query,username):
	# ~ conn = sqlite3.connect("./database/bookstore.db")
	# ~ cursor = conn.cursor()
	# ~ cursor.execute(query,username)
	# ~ conn.commit()
	# ~ print("deleted")
	# ~ conn.close()


# ~ #select_login_db(select_query)
# ~ #delete_table(delete_query, delete_username)
# ~ #select_login_db(select_query)
# ~ #create_table(create_query)
# ~ #insert_login_db(insert_query)


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData
  

insert_query="insert into book(b_id, b_name, b_author, b_publisher, b_price, b_desc, b_isbn, b_img, b_img_small, b_pdf, b_stock) values(?,?,?,?,?,?,?,?,?,?,?)"

def insert_login(query, data_list, image, image_small):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	img_data = convertToBinaryData(image)
	img_data_small = convertToBinaryData(image_small)
	data_list.insert(7, img_data)
	data_list.insert(8, img_data_small)
	data = tuple(data_list)
	cursor.execute(query, data)
	conn.commit()
	if cursor.rowcount:
		print(cursor.rowcount)
	conn.close()

dlist = [343, 'malala', 'someone', 'someone else', 100.20, "this is the book you need right now", "34873847384738743", "path", 5]

insert_login(insert_query, dlist, './static/malala.png', './static/malala_small.png')
