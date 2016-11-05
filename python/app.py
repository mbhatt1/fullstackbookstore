
from __future__ import print_function
import os, sys
from flask import Flask, render_template, send_file, request, flash, redirect, Markup, session
from flick_flask.Database import datab as db
from werkzeug import secure_filename
import time

from datetime import timedelta
import uuid





app = Flask(__name__)
app.secret_key = 'super secret key'

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SESSION_TYPE'] = 'filesystem'
app.jinja_env.autoescape = False
app._static_folder = os.path.join(app.config['UPLOAD_FOLDER'])




@app.before_request
def make_session_permanent():
    session.permanent = False
    app.permanent_session_lifetime = timedelta(minutes=1)


@app.route('/')
def hello():
    return render_template('base.html')

@app.route('/bookStoreFlip.html', methods=['GET', 'POST'])

def bookStoreFlip():
	books = []

	if request.method=='GET':

		if 'status' in session and session['status']==True:
			if 'asking_for_own_books' in session and session['asking_for_own_books'] == True:
				session['asking_for_own_books'] = False
				flash('These are your books')
				return render_template('bookStoreFlip/index.html', username=session['username'], booksFound=db.get_books_by_email(Email=session['username']))
			else:
				return render_template('bookStoreFlip/index.html', username=session['username'], booksFound=db.get_all_books())
		else:
			session['username'] = 'Your Account'
			return render_template('bookStoreFlip/index.html', username='Your Account', booksFound=db.get_all_books())

	if request.method=='POST':
		if 'department' in request.form and request.form['department'] == 'None':
			return redirect('/bookStoreFlip.html')

		if 'department' in request.form:
			books =db.get_books_by_department(Department=request.form['department'])
			flash('Filtered by department')


		if 'status' in session and session['status']==True:
			return render_template('bookStoreFlip/index.html', username=session['username'], booksFound=books)
		else:
			return render_template('bookStoreFlip/index.html', username="Your Account", booksFound=books)
	return 0


@app.route ('/showBook/<bookId>', methods=['GET'])
def  getBookInfo(bookId):

	bookId= int(bookId)
	books = db.get_books_by_Id(Id=bookId)
	flash(repr(books[0].Name))
	return render_template('bookStoreFlip/showBookInfo.html', book=books[0], username=session['username'])


@app.route('/booksListed.html')

def booksListed():
	if 'status' in session and session['status']==True:
		session['asking_for_own_books'] = True
		return redirect('/bookStoreFlip.html')
	else:
		flash('You asked for your books.')
		flash('But you are not logged in.')
		return redirect ('/login.html')


@app.route('/login.html', methods=['GET', 'POST'])

def account():
	if request.method == 'GET':
		if 'status' in session and session['status']==True:
			session['status'] = False
			if 'from login' in session and session['from_login'] == True:
				session['from_login'] = False
			if 'from_loggedon' in session and session ['from_loggedon'] == True:
				session['from_loggedon'] = False
			session['username'] = "Your Account"
		return render_template('bookStoreFlip/login.html')
	if request.method == 'POST':
		username = request.form["username"]
		password = request.form["password"]
		if db.get_seller_email_password(Email=username, passwd=password) == 0:
			session['username'] = username
			session['status'] = True

			return redirect('/loggedon.html')
		if db.get_seller_email_password(Email=username, passwd=password) == -2:
			flash('-2 Username not Found', 'Error:')
			flash('Redirect to <a href="/register.html" class="alert-link">Register Site</a>', 'Info:')
			session['from_login'] = True
			return redirect('/login.html')
		if db.get_seller_email_password(Email=username, passwd=password) == -1:
			flash('-1 Password Error', 'Error:')
			return redirect('/login.html')
	return redirect('/login.html')




@app.route('/register.html', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		if 'from_login' in session and session['from_login'] == True:
			return render_template('bookStoreFlip/register.html')
		else:
			flash('Can\'t access page')
			return redirect('/login.html')

	if request.method == 'POST':
		firstName = request.form["firstname"]
		lastName = request.form["lastname"]
		email = request.form["username"]
		department = request.form["department"]
		password = request.form["pwd1"]
		code = db.set_seller(Email=email, passwd=password, firstName=firstName, lastName=lastName, department=department)
		if code==0:
			flash("Successfully Created")
			return redirect("/login.html")
			
		else:
			flash ("Not Created")
			return redirect("/login.html")

	return redirect("/login.html")


@app.route('/loggedon.html' ,methods=['GET', 'POST'])
def loggedon():
	if 'status' in session and session['status']==True:
		session['from_loggedon'] = True
		res = db.get_all_books()
		res = [x.__dict__ for x in res]
		return render_template('bookStoreFlip/loggedon.html', username=session['username'], booksFound=res)
	else:
		flash('Need to login')
		return redirect('/login.html')




@app.route('/addBook.html', methods=['GET', 'POST'])

def addBook():
	if request.method =='GET':
		if 'from_loggedon' in session and session['from_loggedon'] == True:
			return render_template('bookStoreFlip/addBook.html', username=session['username'])
		else:
			flash('Session has timed out')
			return redirect ('/login.html')

	if request.method == 'POST':
		bookname = request.form['bookname']
		department = request.form['department']
		coursenumber=request.form['coursenumber']
		
		photo = request.files['photo']
		filename = str(uuid.uuid4())+photo.filename
		photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        error = db.set_book(Name =bookname, Seller_email = session['username'], department = department, course = coursenumber, photoid=os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        if error == -2:
        	flash('Same Book Listed')
        	return redirect('/addBook.html')
        else:
        	flash('Book Added')
        	return redirect('/bookStoreFlip.html')


@app.route('/uploads/<filename>')
def sendfile(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    
    app.run(host='0.0.0.0', port=port, debug=True)
