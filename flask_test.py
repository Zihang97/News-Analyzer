from flask import Flask, escape, request, redirect, url_for, render_template
from database import *
from news import *

app = Flask(__name__)

@app.route('/register/', methods=['GET','POST'])
def regist():
	if request.method =='POST':   
		username = request.form['username']  
		password = request.form['password']  
		repassword = request.form['repassword']
		users = GETUSER()
		if password == repassword:
			if username in users:
				return 'user already exist'
			else:
				insertuser(username, password)
				createtable(username)
				#after register userinformation is saved in user list as a dictionary
				return redirect('/')
				#user will be redirect to login page after register.
		else:
		  return('password should be identical to repassword')
	return render_template('regist.html')

@app.route('/', methods=['GET','POST'])
def index():
	return render_template('index.html')

#this is the login page, we post our information and it can check wheter our information is in user list
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method =='POST': 
		username = request.form['username']
		password = request.form['password']
		users = GETUSER()
		if username in users:
			if password == users[username]:
				return redirect(url_for('main', name = username))
			else:
				return render_template('login_return.html', text = 'Wrong Password!')
		else:
			return render_template('login_return.html', text = 'Username Not Found, please register first!')
	return render_template('login.html')
    #check if we have user information in our list, if we do the user is successfully login.
    #else, he or she either does not regist or enters wrong information

@app.route('/mainpage/<name>', methods = ['GET', 'POST'])
def main(name):
	return render_template('mainpage.html', name = name)

@app.route('/profile/<name>', methods = ['GET', 'POST'])
def profile(name):
	filenames = GETALL(password, name)
	return render_template('profile.html', name = name, filenames = filenames)

@app.route('/file/display/<name>/<filename>', methods = ['GET', 'POST'])
def display(name, filename):
	file, content = GET(password, name, filename)
	return render_template('display_file.html', name=name, file=file, content=content)

# @app.route('/login',methods = ['POST', 'GET'])
# def login():
# 	if request.method == 'POST':
# 		user = request.form['name']
# 	else:
# 		user = request.args.get('name')
# 	return redirect(url_for('hello_world', name = user))

@app.route('/uploader/<name>', methods = ['GET', 'POST'])
def uploader(name):
	if request.method == 'POST':
		f = request.files['file']
		f.save('./File_buffer/' + f.filename)
		POST(password, name, './File_buffer/' + f.filename, f.filename)
		return render_template("return.html", name=name)

@app.route('/file/file_update/<name>', methods = ['GET', 'POST'])
def update(name):
	return render_template('update.html', name=name)

@app.route('/file/file_update_result/<name>', methods = ['GET', 'POST'])
def updating(name):
	if request.method == 'POST':
		creator = request.form['author']
		new_content = request.form['new_content']
		PUT(password, name, creator, new_content)
	return redirect(url_for('main', name = name))

@app.route('/file/file_delete/<name>', methods = ['GET', 'POST'])
def delete(name):
	return render_template('delete.html', name=name)

@app.route('/file/file_deleting/<name>', methods = ['GET', 'POST'])
def deleting(name):
	if request.method == 'POST':
		creator = request.form['author']
		DELETE(password, name, creator)
	return redirect(url_for('main', name = name))

@app.route('/file/file_query/<name>', methods = ['GET', 'POST'])
def query(name):
	if request.method == 'POST':
		keyword = request.form['keyword']
		pass_key = keyword + ' '
		results = search(password, name, pass_key)
	return render_template('display.html', name=name, results = results, keyword = pass_key)


@app.route('/news/<name>', methods = ['GET', 'POST'])
def news(name):
	return render_template('news_search.html', name=name)

@app.route('/news/query/<name>', methods = ['GET', 'POST'])
def news_query(name):
	if request.method == 'POST':
		keyword = request.form['news_keyword']
		pagenum = request.form['page']
		title, date, link = search_news(keyword, int(pagenum))
	if title != '':
		return render_template('news_display.html', name=name,title=title, date=date, link=link)
	else:
		return render_template('news_display.html', name=name, title='No file matched', date=date, link=link)


if __name__ == '__main__':
	app.run()
