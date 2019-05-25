from flask import Flask, request, redirect, url_for, render_template, jsonify, send_from_directory
from functions import *
import pandas as pd
import os
import string
import random

# This line sets the app directory as the working directory
app = Flask(__name__)

# The home route
@app.route('/', methods=['GET'])
def home_page():
    # Show the index page
    return render_template('index.html')

# A route to the test page that simply returns hello
@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello, World!'
	
# The dosomething route
@app.route('/dosomething', methods=['GET'])
def dosomething():
    # Show something
    return str(return_something())
	
# The dosomething2 route
@app.route('/dosomething2', methods=['GET', 'POST'])
def dosomething2():
    # If the request is a post request
    if request.method == 'POST':

        url1 = request.form['url1']
        url2 = request.form['url2']
        increment_string1 = '-or'
        increment_string2 = ''
        total_pages = request.form['total_pages']
        increment = 10
        site = request.form['site']
        filename = ''
		
        filename = LDA(site, url1, url2, increment_string1, increment_string2, total_pages, increment)
		
        # # Return the result
        # #return 'The predicted Sale Price of this house is: ' + str(round(result, 2)) + '. \n <button><a href="/plot/' + filename + '">See Sales Price Distribution</a></button><p></p>'
        #return '<p></p> <img src="static/' + filename + '2.png"><p></p><p></p> <a href="' + filePath + '/static/' + filename + '1.html">LDA Visualisation</a><p></p>'
		
        #return render_template(filename + '1.html')
        ldafile = filename + '1.html'
        wordcloud = 'static/' + filename + '2.png'
        return render_template('ShowResult.html',ldafile=ldafile, wordcloud=wordcloud)
    else:
        # Show the form page
        return render_template("dosomethingform.html")


if __name__ == '__main__':
    # Let the console know that the load is successful
    print("loaded OK")

    # Set to debug mode
    app.run(debug=True)