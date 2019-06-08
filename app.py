from flask import Flask, request, redirect, url_for, render_template, jsonify, send_from_directory
from functions import *
import pandas as pd
import os
import string
import random
from celery import Celery

# This line sets the app directory as the working directory
app = Flask(__name__)

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# The home route
@app.route('/', methods=['GET'])
def home_page():
	# Show the index page
	return redirect('/dosomething2')
	
@celery.task
def my_background_task(site, url1, url2, increment_string1, increment_string2, total_pages, increment, filename):
	LDA(site, url1, url2, increment_string1, increment_string2, total_pages, increment, filename)
	return result

# The dosomething route
@app.route('/showresult', methods=['GET'])
def showresult():
	filename = request.args.get('filename')
	ldafile = filename + '1.html'
	wordcloud = 'static/' + filename + '2.png'

	if not os.path.exists('templates/LDAhtmls/' + ldafile):
		return 'File is not ready yet!'

	# Show something
	return render_template('ShowResult.html', ldafile=ldafile, wordcloud=wordcloud)


# The dosomething2 route
@app.route('/dosomething2', methods=['GET', 'POST'])
def dosomething2():
	# If the request is a post request
	if request.method == 'POST':

		url1 = request.form['url1']
		url2 = request.form['url2']
		increment_string1 = request.form['increment_string1']
		increment_string2 = ''
		total_pages = request.form['total_pages']
		increment = request.form['increment']
		site = request.form['site']
		filename = ''
		for i in range(4):
			filename = filename + random.choice(string.ascii_letters)

		return render_template('waiting.html', url1=url1, url2=url2, increment_string1=increment_string1,
							   increment_string2=increment_string2, total_pages=total_pages, increment=increment,
							   site=site, filename=filename)
	else:
		# Show the form page
		return render_template("dosomethingform.html")


# The process route
@app.route('/process', methods=['POST'])
def process():
	url1 = request.form['url1']
	url2 = request.form['url2']
	increment_string1 = request.form['increment_string1']
	increment_string2 = request.form['increment_string2']
	total_pages = int(request.form['total_pages'])
	increment = int(request.form['increment'])
	site = request.form['site']
	filename = request.form['filename']

	if os.path.exists('templates/LDAhtmls/' + filename + '1.html'):
		return 'duplicate'

	task = my_background_task.delay(site, url1, url2, increment_string1, increment_string2, total_pages, increment, filename)

	return 'done'


if __name__ == '__main__':
	# Let the console know that the load is successful
	print("loaded OK")

	# Set to debug mode
	app.run(debug=True)