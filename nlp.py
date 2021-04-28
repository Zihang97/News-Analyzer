import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize
from nltk.probability import FreqDist

# nltk.download('vader_lexicon')
# nltk.download('punkt')

def sentiment_analysis(text):
	analyzer = SentimentIntensityAnalyzer()
	senti = analyzer.polarity_scores(text)
	neg = senti['neg']
	neu = senti['neu']
	pos = senti['pos']
	max_score = max(neg, neu, pos)

	for sent, score in senti.items():
		if score == max_score:
			return sent


def search_nlp(keyword, text): 
	words = word_tokenize(text) 
	words = [word.lower() for word in words]
	freqdist = FreqDist(words) 

	keyfreq = freqdist[keyword.lower()] 

	return keyfreq
