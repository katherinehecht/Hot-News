#! /usr/bin/env python3
# Hot News
# Katherine Hecht, Jack Hill, Rick Stefanik
# _article_database.py
# November 2, 2018

# imports
from operator import itemgetter
import unittest
import requests
import json
import math
import datetime
from enum import Enum, auto

# define state info mode
class StateInfoMode(Enum):
	BOTH = auto()
	USER_ARTICLES = auto()
	API_ARTICLES = auto()

# create article datavase
class _article_database:
	def __init__(self):
		self.articles_title = {} # based on title
		self.states = [] # each state
		self.URL = 'https://newsapi.org/v2/everything?'

		# declare several API keys to avoid overuse 
		self.API_KEY = '29564cec822349e18cd6fa7fe5ec4bd8'
		self.API_KEYS = ['e77901f9bbb048abb491da93c31c8cf0', 'eddcbcebef474f1ea44aa3235b4da71b', '5007c552320d45c5a2ead69dde3ec944', '29564cec822349e18cd6fa7fe5ec4bd8', '7f2f902a169a4ef8a12fa1850eae47d2', '0e9d46e857ea40ef88351e07d2a9b5f0', 'ac7e3d4478f54722bef4b1edbd96304d', 'dc144ea3dc104ccf987920e4f4475c27', '0a2d5799831f46ec838323fe6c6c18a5', 'bc25329296204311bcdfa1a792e5e9d0']
		#self.API_KEYS = ['5007c552320d45c5a2ead69dde3ec944', '29564cec822349e18cd6fa7fe5ec4bd8']
		#self.API_KEYS = ['e77901f9bbb048abb491da93c31c8cf0', 'eddcbcebef474f1ea44aa3235b4da71b']

		# load states from states.csv
		self.load_states()

	# Load all the states and their appreviations from a csv file into a list of tuples
	def load_states(self):
		f = open("states.csv")
		for line in f:
			line = line.rstrip().split(', ')
			self.states.append((line[0], line[1]))
		f.close()

	# Generates a dictionary for a certain day that contains each state as a key
	# that has the total number of results for the given keyword and 5 links to articles as values
	def get_stateInfo_keyword(self, keywords, day, type):
		# define type to be either API articles, user articles, or both
		if type == "BOTH":
			type = StateInfoMode.BOTH
		elif type == "USER":
			type = StateInfoMode.USER_ARTICLES
		elif type == "API":
			type = StateInfoMode.API_ARTICLES
		
		# initialize states 
		ret = {}
		for state in self.states:
			ret[state[0]] = {}
			ret[state[0]]['value'] = 0 # name of state
			ret[state[0]]['links'] = []

		# iterate through keywords
		for keyword in keywords:
			# Looks through user uploaded articles
			if type == StateInfoMode.BOTH or type == StateInfoMode.USER_ARTICLES:
				for title in self.articles_title:
					article = self.articles_title[title]
					if article['date'] == day:
						lowerArticleKeywords = [a.lower() for a in article['keywords']]
						for state in self.states:
							if ((state[0].lower() in article['content'].lower()) or (state[0].lower() in article['title'].lower()) or (state[0].lower() in lowerArticleKeywords)) and ((keyword.lower() in article['content'].lower()) or (keyword.lower() in article['content'].lower()) or (keyword.lower() in article['title'].lower()) or (keyword.lower() in article['title'].lower()) or (keyword.lower() in lowerArticleKeywords) or (keyword.lower() in lowerArticleKeywords)):
								ret[state[0]]['value']+= 1
								ret[state[0]]['links'].append(article['link'])

			# Looks through articles obtained by using news api
			if type == StateInfoMode.BOTH or type == StateInfoMode.API_ARTICLES:
				for state in self.states:
						try:
							# build the url to query
							url = self.URL + 'q="' + keyword.replace(' ','%20').replace('"', '') + '"+' + '("' + state[0].replace(' ', '%20') + '"OR"' + state[1] + '")&apiKey=' + self.API_KEY + '&pageSize=5&from=' + str(day) + '&to=' + str(day)
							r = requests.get(url)

							# check if the API has reached too many requests 
							while r.status_code == 429:
								if len(self.API_KEYS) == 0:
									return ret
								# replace  API key with new id
								self.API_KEY = self.API_KEYS[0]
								self.API_KEYS.pop(0)
								# rebuild API
								url = self.URL + 'q="' + keyword.replace(' ','%20').replace('"', '') + '"+' + '("' + state[0].replace(' ', '%20') + '"OR"' + state[1] + '")&apiKey=' + self.API_KEY + '&pageSize=5&from=' + str(day) + '&to=' + str(day)
								r = requests.get(url)

							if r.status_code == 429 or r.status_code == 404:
								continue
					
							resp = json.loads(r.content.decode())
							if ['status'] == 'error':
								continue
							# get articles from response
							articles = resp['articles']
							for article in articles:
								date = article['publishedAt']
								article_url = article['url']
								ret[state[0]]['links'].append(article_url)
					
							# accumulate total results
							totalResults = resp['totalResults']
							ret[state[0]]['value'] += totalResults

						except Exception as e:
							print(str(e))
							pass
		return ret

	# Returns a user uploaded article specified by title
	def get_userArticle(self, title):
		if title not in self.articles_title.keys():
			return None
		return self.articles_title[title]

	# Returns all user uploaded articles
	def get_all_userArticles(self):
		ret = []
		for title in self.articles_title:
			ret.append(self.articles_title[title])
		return ret

	# Puts a user uploaded article into the dictionaries
	def put_userArticle_title(self, article):
		title = article['title']
		source = article['source']
		keywords = article['keywords']

		self.articles_title[title] = article

	# Puts a list of user articles into the dictionaries containing them
	def post_userArticles(self, articles):
		for article in articles:
			self.put_userArticle_title(article)

	# Deletes a user article from the dictionaries based in its title
	def delete_userArticle(self, titleToDelete):
            del self.articles_title[titleToDelete]

	# Deletes all user uploaded articles
	def delete_all_userArticles(self):
		self.articles_title = {} # based on title

	# Generates an article in the proper format
	def makeArticle(self, title, source, link, content, date, keywords=None):
		# initalize dictionary of article values
		ret = {}
		ret['keywords'] = []
		if keywords is not None:
			ret['keywords'] = keywords.copy()
		ret['title'] = title
		ret['source'] = source
		ret['link'] = link
		ret['content'] = content
		ret['date'] = date
		return ret

	# Takes a day as a string and return the next day as a string
	def getNextDay(self, day):
		day = day.split("-")
		date = datetime.datetime(int(day[0]), int(day[1]), int(day[2]))
		date += datetime.timedelta(days=1)
		return str(date).split(" ")[0]

	# Takes a day as a string and returns the previous day as a string
	def getPrevDay(self, day):
		day = day.split("-")
		date = datetime.datetime(int(day[0]), int(day[1]), int(day[2]))
		date += datetime.timedelta(days=-1)
		return str(date).split(" ")[0]

	# Calls get_stateInfo_keyword for a range of days
	def get_stateInfo_range(self, keywords, startDay, daysPrev, type=None):
		ret = {"result": "success"}
		ret['dates'] = {}
		currDay = startDay
		for i in range(daysPrev):
			ret['dates'][currDay] = self.get_stateInfo_keyword(keywords, currDay, type)
			currDay = self.getPrevDay(currDay)

		return ret

if __name__ == "__main__":
	# initialize database
	adb = _article_database()
	dateRange = "2018-11-03"
	keywords = ["election", "politics"]


	articles = [ {
        "title" : "fake title 2",
        "source" : "fake source 2",
        "keywords" : ["election"],
        "link" : "https://fakelink2.com",
        "content" : "this is from California",
        "date" : "2018-11-05"
    },
    {
        "title" : "fake title 3",
        "source" : "fake source 3",
        "keywords" : ["politics"],
        "link" : "https://fakelink.com",
        "content" : "this is from New York",
        "date" : "2018-11-04"
    }
    ]
	adb.post_userArticle(articles)
	ret = adb.get_stateInfo_range(["politics", "election"], "2018-11-05", 2, "USER")
	with open("api_data.json", "w") as f:
		f.write(json.dumps((adb.get_newsArticle_keyword_and_source(["Election"], "cnn"))))
