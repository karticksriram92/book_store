from flask import Flask, session, redirect, Blueprint, render_template
import sqlite3

#payment-stripe
# ~ stripe.api_key=app.app.config["STRIPE_SECRET_KEY"]

# ~ cart_page = Blueprint('cart_page', __name__, template_folder='templates')

# ~ @cart_page.route("/cart", methods=['POST','GET'])
# ~ def create_checkout_session():
	#dont uncomment.
	# ~ checkout_session = stripe.checkout.Session.create(payment_method_types=['card'],line_items=[{'price_data' : {'currency' : 'inr','unit_amount' : 500,'product_data' : {'name' : 'name of the product',},},'quantity' : 1,},], mode='payment',success_url=my_domain + '/success.html', cancel_url=my_domain + '/cancel.html',)
	# ~ checkout_session = stripe.checkout.Session.create(payment_method_types=['card'],line_items=[{
                    # ~ "name": "Learn Python",
                    # ~ "quantity": 1,
                    # ~ "currency": "inr",
                    # ~ "amount": "25000",
                # ~ },{
                    # ~ "name": "Learning SciPy",
                    # ~ "quantity": 1,
                    # ~ "currency": "inr",
                    # ~ "amount": "30000",
                # ~ },], mode='payment',success_url=request.host_url + 'success', cancel_url= request.host_url + 'cart',)
	
	# ~ return render_template('cart.html', checkout_session_id=checkout_session['id'], checkout_public_key=app.config['STRIPE_PUBLIC_KEY'])

cart_page = Blueprint('cart_page', __name__, template_folder='templates')

@cart_page.route("/cart", methods=['POST','GET'])
def cart_management():
	if 'uid' in session:
		cart_items = get_cart(session['uid'])
		print(cart_items)
	return render_template('cart.html')
		 
# ~ def get_cart(u_id):
	# ~ conn = sqlite3.connect("./database/bookstore.db")
	# ~ conn.row_factory = dict_factory
	# ~ cursor = conn.cursor()
	# ~ cursor.execute("select u_cart from book where b_id=?",(b_id_list,))
	# ~ result=cursor.fetchone()
	# ~ if result:
		# ~ conn.close()
		# ~ return result[0]
	# ~ conn.close()
