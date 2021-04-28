from flask import Flask, escape, request, redirect, url_for, render_template
from database import *
from news import *

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def main():
	return render_template('mainpage.html')

# @app.route('/login',methods = ['POST', 'GET'])
# def login():
# 	if request.method == 'POST':
# 		user = request.form['name']
# 	else:
# 		user = request.args.get('name')
# 	return redirect(url_for('hello_world', name = user))

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
	if request.method == 'POST':
		f = request.files['file']
		f.save('./File_buffer/' + f.filename)
		POST(password, './File_buffer/' + f.filename, f.filename)
		return render_template("return.html")

@app.route('/file/file_update/', methods = ['GET', 'POST'])
def update():
	return render_template('update.html')

@app.route('/file/file_update_result/', methods = ['GET', 'POST'])
def updating():
	if request.method == 'POST':
		creator = request.form['author']
		new_content = request.form['new_content']
		PUT(password, creator, new_content)
	return render_template('mainpage.html')

@app.route('/file/file_delete/', methods = ['GET', 'POST'])
def delete():
	return render_template('delete.html')

@app.route('/file/file_deleting/', methods = ['GET', 'POST'])
def deleting():
	if request.method == 'POST':
		creator = request.form['author']
		DELETE(password, creator)
	return render_template('mainpage.html')

@app.route('/file/file_query/', methods = ['GET', 'POST'])
def query():
	if request.method == 'POST':
		keyword = request.form['keyword']
		pass_key = keyword + ' '
		results = search(password, pass_key)
	return render_template('display.html', results = results, keyword = pass_key)


@app.route('/news', methods = ['GET', 'POST'])
def news():
	return render_template('news_search.html')

@app.route('/news/query', methods = ['GET', 'POST'])
def news_query():
	if request.method == 'POST':
		keyword = request.form['news_keyword']
		pagenum = request.form['page']
		title, date, link = search_news(keyword, int(pagenum))
	if title != '':
		return render_template('news_display.html', title=title, date=date, link=link)
	else:
		return render_template('news_display.html', title='No file matched', date=date, link=link)


if __name__ == '__main__':
	app.run()
