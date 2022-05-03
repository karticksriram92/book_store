import sqlite3

select_query="select count(*) from login where name=? and password=?"
insert_query="insert into login(name, password) values('karticksriram','sriram20')"

def login_db(query):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute(query)
	conn.commit()
	conn.close()

login_db(insert_query)
