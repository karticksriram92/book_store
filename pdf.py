from flask import Flask, send_from_directory, Blueprint
import os

pdf_page = Blueprint('pdf_page', __name__, template_folder="templates")

@pdf_page.route('/pdf')
def showPdf():
	workdir = os.path.abspath(os.getcwd())
	fpath = workdir + '/static/pdf/'
	return send_from_directory(fpath, 'learn_python.pdf')
