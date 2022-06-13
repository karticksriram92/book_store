from flask import Flask, session, redirect, Blueprint, render_template
import sqlite3

cart_page = Blueprint('cart_page', __name__, template_folder='templates')

@cart_page.route("/cart", methods=['POST','GET'])
def cart_management():
	 
