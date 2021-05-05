import pymysql
from extract_pdf_data import *
from nlp import *
from pdfreader import *

password = "root"

def createtable(username, password = password):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()

	tablename = 'file_' + username

	sql = 'drop table if exists ' + tablename
	cursor.execute(sql)

	sql = 'CREATE TABLE ' + tablename + ' (filename VARCHAR(40), create_time VARCHAR(40), modified_time VARCHAR(40), content TEXT, sentiment VARCHAR(10))'
	cursor.execute(sql)

	db.commit()
	 
	db.close()


def POST(password, username, fileaddr, filename):
	info_dict = extract_data(fileaddr)
	content = parse(fileaddr)
	tablename = 'file_' + username

	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()
	
	create_time = info_dict['create_time']
	mod_time = info_dict['modified_time']
	senti = sentiment_analysis(content)

	sql = 'insert into ' + tablename + ' (filename, create_time, modified_time, content, sentiment) values(%s, %s, %s, %s, %s)'
	cursor.execute(sql, (filename, create_time, mod_time, content, senti))

	db.commit()
	
	db.close()


def insertuser(username, word, password=password):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()

	sql = 'insert into user (username, password) values(%s, %s)'
	cursor.execute(sql, (username, word))

	db.commit()
	
	db.close()


def GET(password, username, filename):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()
	tablename = 'file_' + username

	sql = "select * from " + tablename + " where filename=%s"
	cursor.execute(sql, (filename))
	results = cursor.fetchone()
	
	filename = results[0]
	content = results[3]
	 
	db.close()

	return [filename, content]

def GETALL(password, username):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()
	tablename = 'file_' + username

	sql = "select * from " + tablename
	cursor.execute(sql)
	results = cursor.fetchall()
	
	filenames = []
	for row in results:
		filenames.append(row[0])
	 
	db.close()

	return filenames

def GETUSER(password=password):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()

	sql = "select * from user"
	cursor.execute(sql)
	results = cursor.fetchall()
	
	users = {}
	for row in results:
		users[row[0]] = row[1]
	 
	db.close()

	return users

def search(password, username, keyword):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()
	tablename = 'file_' + username

	sql = "select * from " + tablename
	cursor.execute(sql)
	results = cursor.fetchall()
	out = []
	for row in results:
		dic = {}
		dic['filename'] = row[0]
		cnt = row[3].count(keyword)
		dic['frequency'] = cnt
		index = 0
		prev = -250
		cur = []
		while index != -1:
			index = row[3].find(keyword, index, len(row[3]) - 1)
			if index != -1:
				if index >= prev + 250:
					para = row[3][max(0, index - 250):index + 250]
					cur.append(['...' + para + '...', sentiment_analysis(para)])
					prev = index
				index += 1
		dic['content'] = cur
		out.append(dic)
	return out


def PUT(password, username, filename, new_content):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()
	tablename = 'file_' + username

	sql = "update " + tablename + " set content=%s where filename=%s"

	cursor.execute(sql, (new_content, filename))
	db.commit()


	db.close()


def DELETE(password, username, filename):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()
	tablename = 'file_' + username

	sql = "delete from " + tablename + " where filename=%s"
	cursor.execute(sql, (filename))

	db.commit()
	 
	db.close()


# createtable(password, 'hhh')
# POST(password, './File_buffer/Zoom.pdf')
# print(GETUSER())
# print(search(password, 'you'))