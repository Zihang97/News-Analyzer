import feedparser
from nlp import *

def news_create():
	feedcnn = feedparser.parse("http://rss.cnn.com/rss/cnn_topstories.rss")
	feed_nytimes = feedparser.parse("https://rss.nytimes.com/services/xml/rss/nyt/World.xml")
	
	return feedcnn, feed_nytimes

def search_news(keyword, pagenum):
	feedcnn, feed_nytimes = news_create()
	for i in range(pagenum//2):
		entrycnn = feedcnn.entries[i]
		entry_nytimes = feed_nytimes.entries[i]
		if search_nlp(keyword, entrycnn.title) > 0:
			return entrycnn.title, entrycnn.published, entrycnn.link
		if search_nlp(keyword, entry_nytimes.title) > 0:
			return entry_nytimes.title, entry_nytimes.published, entry_nytimes.link
	return '', '', ''

# print(search_news('US', 20))
