import sqlite3

create_query="create table user(username varchar(30) primary key , password varchar(30), first_name varchar(30), last_name varchar(30), email varchar(30), address varchar(100))"
select_query="select * from user"
drop_query="drop table user"
select_count_query="select count(*) from login where name=? and password=?"
insert_query="insert into login(name, password) values('karticksriram','sriram20')"
delete_query="delete from user where username=?"
delete_username=("karticksriram",)

def insert_login(query):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute(query)
	conn.commit()
	if cursor.rowcount:
		print(cursor.rowcount)
	conn.close()
	
def select_login(query):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute(query)
	data = cursor.fetchall()
	for row in data:
		print(row)
	conn.close()
	
data=('karticksriram','sriram20')

def select_count_login(query,ldata):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute(query,ldata)
	print(cursor.fetchone()[0])
	conn.close()

#select_count_login_db(select_count_query,data)


def create_table(query):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute(query)
	print("tabel created")
	conn.close()

def delete_table(query,username):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute(query,username)
	conn.commit()
	print("deleted")
	conn.close()


#select_login_db(select_query)
#delete_table(delete_query, delete_username)
#select_login_db(select_query)
#create_table(create_query)
#insert_login_db(insert_query)
