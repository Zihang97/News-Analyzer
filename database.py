import pymysql
from extract_pdf_data import *
from nlp import *
from pdfreader import *

password = "*************"

def createtable(password):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()
	
	cursor.execute('drop table if exists files')

	sql = "CREATE TABLE files (author VARCHAR(40), create_time VARCHAR(40), modified_time VARCHAR(40), content TEXT, sentiment VARCHAR(10))"
	 
	cursor.execute(sql)
	 
	db.close()


def POST(password, fileaddr, filename):
	info_dict = extract_data(fileaddr)
	content = parse(fileaddr)

	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()
	
	auth = filename
	create_time = info_dict['create_time']
	mod_time = info_dict['modified_time']
	senti = sentiment_analysis(content)

	sql = "insert into files (author, create_time, modified_time, content, sentiment) values(%s, %s, %s, %s, %s)"
	cursor.execute(sql, (auth, create_time, mod_time, content, senti))

	db.commit()
	
	db.close()


def GET(password, creator):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()

	sql = "select * from files where author=%s"
	cursor.execute(sql, (creator))
	results = cursor.fetchone()
	
	creator = results[0]
	content = results[3]
	sentiment = results[-1]
	 
	db.close()

	return [creator, content, sentiment]

def search(password, keyword):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()

	sql = "select * from files"
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


def PUT(password, filename, new_content):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()

	sql = "update files set content=%s where author=%s"

	cursor.execute(sql, (new_content, creator))
	db.commit()


	db.close()


def DELETE(password, filename):
	db = pymysql.connect(host = "localhost", user = "root", password = password, database = "news_analyzer")
	 
	cursor = db.cursor()

	sql = "delete from files where author=%s"
	cursor.execute(sql, (creator))

	db.commit()
	 
	db.close()


# createtable(password)
# POST(password, './File_buffer/Zoom.pdf')
# print(search(password, 'you'))
