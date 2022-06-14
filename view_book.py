from flask import Flask, Blueprint, request, render_template, session
from comment_form import Commentform
from datetime import datetime
import sqlite3

view_book_page = Blueprint('view_book_page', __name__, template_folder='templates')

@view_book_page.route('/books/<b_id>', methods=['POST', 'GET'])
def view_book(b_id):
	form = Commentform()
	check_status=False
	success=False
	if form.validate_on_submit():
		date_now = datetime.now().date()
		print("validating")
		if 'uid' not in session:
			review_data=(None, b_id, form.name.data, form.email.data , date_now, form.comment.data, form.rstar.data, 'yes')
			check_status = check_review(b_id, form.email.data)
		else:
			user_data = get_user_data(session['uid'])
			review_data=(session['uid'], b_id, user_data['u_username'], user_data['u_email'], date_now, form.comment.data, form.rstar.data, 'yes')
			check_status = check_review(b_id, user_data['u_email'])
		if check_status:
			if add_review(review_data):
				form=Commentform(formdata=None)
				success=True
		else:
			print("same username or email.")
			pass
	book_data=get_book(b_id)
	reviews = get_review(b_id)
	reviews_data, star_rating_dict = process_review(reviews)
	avg_r, tcount=get_avg_rating(star_rating_dict)
	#for updating book avg rating and total ratings
	if not check_status:
		update_ratings(avg_r, tcount, b_id)
	ratings_bar = make_ratings(star_rating_dict, tcount)
	ratings=struct_ratings(avg_r, tcount)
	return render_template('view_book.html', book_data=book_data, ratings_bar=ratings_bar, form=form, ratings=ratings, reviews_data=reviews_data, success=success)
	
def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def get_book(b_id_list):
	conn = sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	cursor.execute("select * from book where b_id=?",(b_id_list,))
	rows = cursor.fetchall()
	conn.close()
	return rows[0]

def get_avg_rating(srdict):
	total_rating = 0.0
	num_of_rating = 0.0
	avg_rating = 0.0
	for key, item in srdict.items():
		total_rating += key * item
		num_of_rating += item
	if num_of_rating:
		avg_rating = round(total_rating/num_of_rating,1)
	return avg_rating, int(num_of_rating)

def struct_ratings(rating, count):
	rdict={}
	rdict['org']= rating
	rdict['count']= count
	rdict['full']= str(rating).split('.')[0]
	rdict['half']= True if int(str(rating).split('.')[1])>=5 else False
	return rdict
	
def make_ratings(srdict, total_count):
	percentage_dict={ 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0 }
	if not total_count:
		return percentage_dict
	for i in range(1,6):
		percentage_dict[i]=int((srdict[i]/total_count)*100)
	return percentage_dict
	

def check_review(book_id, email):
	status=True
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("select count(*) from review where b_id=? and email=?", (book_id, email))
	if(cursor.fetchone()[0]):
		# ~ status["username"]="Username exists already"
		status=False
	conn.close()
	return status

def add_review(rdata):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("insert into review(u_id, b_id, name, email, date, review, stars, approval) values(?,?,?,?,?,?,?,?)", rdata)
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()
	
def get_review(book_id):
	conn = sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	cursor.execute("select * from review where b_id=?",(book_id,))
	rows = cursor.fetchall()
	conn.close()
	return rows

def process_review(r_data):
	stars_dict={ 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0 }
	review_list=[]
	for rdict in r_data:
		if rdict['approval'] == 'yes':
			review_list.append(rdict)
	for item in review_list:
		item['date']=datetime.strptime(item['date'], '%Y-%m-%d')
		item['date']=item['date'].strftime("%d")+' '+item['date'].strftime("%b")+' '+item['date'].strftime("%Y")
		for i in range(1,6):
			if item['stars'] == i:
				stars_dict[i] += 1
				# ~ stars_dict['total'] +=1
	# ~ print(stars_dict)
	return review_list, stars_dict
	
def get_user_data(u_id):
	conn = sqlite3.connect("./database/bookstore.db")
	conn.row_factory = dict_factory
	cursor = conn.cursor()
	cursor.execute("select * from user where u_id=?",(u_id,))
	rows = cursor.fetchall()
	conn.close()
	return rows[0]

def update_ratings(avg_rating, total_count, book_id):
	conn = sqlite3.connect("./database/bookstore.db")
	cursor = conn.cursor()
	cursor.execute("update book set b_avg_rating=?, b_total_rating=? where b_id=?", (avg_rating, total_count, book_id))
	conn.commit()
	if(cursor.rowcount):
		conn.close()
		return True
	conn.close()
