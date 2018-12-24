#! /usr/bin/env python3

# Katherine Hecht, Jack Hill, Rick Stefanik
# _article_database.py
# November 2, 2018

from operator import itemgetter
import unittest
import requests
import json
import math
import datetime


from enum import Enum, auto

class StateInfoMode(Enum):
	BOTH = auto()
	USER_ARTICLES = auto()
	API_ARTICLES = auto()

class _article_database:
	def __init__(self):
		self.articles_title = {} # based on title
		self.states = [] # each state
		self.URL = 'https://newsapi.org/v2/everything?'
		self.API_KEY = 'dc144ea3dc104ccf987920e4f4475c27'
		#self.API_KEY = '0a2d5799831f46ec838323fe6c6c18a5'
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
		if type == "BOTH":
			type = StateInfoMode.BOTH
		elif type == "USER":
			type = StateInfoMode.USER_ARTICLES
		elif type == "API":
			type = StateInfoMode.API_ARTICLES
		ret = {}
		for state in self.states:
			ret[state[0]] = {}
			ret[state[0]]['value'] = 0 # name of state
			ret[state[0]]['links'] = []

		for keyword in keywords:
			# Looks through user uploaded articles
			
			if type == StateInfoMode.BOTH or type == StateInfoMode.USER_ARTICLES:
				for title in self.articles_title:
					article = self.articles_title[title]
					if article['date'] == day:
						for state in self.states:
							if state[0] in article['content'] or state[1] in article['content'] or state[0] in article['title'] or state[1] in article['title'] or state[0] in article['keywords'] or state[1] in article['keywords']:
								ret[state[0]]['value']+= 1
								ret[state[0]]['links'].append(article['link'])
								# ret[state[0]]['links'].append(article['content'])

			# Looks through articles obtained by using news api
			if type == StateInfoMode.BOTH or type == StateInfoMode.API_ARTICLES:
				numstates = 1
				for state in self.states:
					if numstates > 0:
						numstates -= 1
						try:
							url = self.URL + 'q="' + keyword.replace(' ','%20').replace('"', '') + '"+' + '("' + state[0].replace(' ', '%20') + '"OR"' + state[1] + '")&apiKey=' + self.API_KEY + '&pageSize=5&from=' + str(day) + '&to=' + str(day)
							r = requests.get(url)
							resp = json.loads(r.content.decode())
							if ['status'] == 'error':
								continue
							totalResults = resp['totalResults']
							ret[state[0]]['value'] += totalResults
							for i in range(1, 2): # range(1, 11)
								page_url = url + '&page=' + str(i)
								r = requests.get(page_url)
								resp2 = json.loads(r.content.decode())
								resp = resp2['articles']
	
								for article in resp:
									date = article['publishedAt']
									article_url = article['url']
									ret[state[0]]['links'].append(article_url)
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

	# Gets a list of articles based on both keyword and source
	def get_newsArticle_keyword_and_source(self, keywords, source):
		ret = {'result' : 'success'}
		ret['articles'] = []
		for keyword in keywords:
			url = self.URL + 'q=' + keyword.replace(' ','%20').replace('"', '') + '&apiKey=' + self.API_KEY + '&pageSize=100&sources=' + source
			print(str(url))
			r = requests.get(url)
			resp = json.loads(r.content.decode())
			if ['status'] == 'error':
				return {'result': 'error'}
			#cprint(str(resp))
			totalResults = resp['totalResults']
			for i in range(1, min(11, (totalResults // 100) + 2)): # range(1, 11)
				page_url = url + '&page=' + str(i)
				r = requests.get(page_url)
				resp2 = json.loads(r.content.decode())
				print(resp2)
				resp = resp2['articles']

				for each_article in resp:
					article = {}
					article['title'] = each_article['title']
					article['source']= each_article['source']['name']
					article['content'] = ""
					if each_article['content'] is not None:
						article['content'] = each_article['content'].replace('"', "'")
					article['link'] = each_article['url']
					article['date'] = each_article['publishedAt'][:10]
					article['keywords'] = []
					if article['content'] is not None:
						article['keywords'] = [a.replace(".", "").replace(",", "") for a in article['content'].split()]
					ret['articles'].append(article)
		return ret

	# Gets a list of articles only based on their source
	def get_newsArticle_source(self, source):
		ret = {'result' : 'success'}
		ret['articles'] = []
		url = self.URL + 'apiKey=' + self.API_KEY + '&pageSize=100&sources=' + source
		#url = self.URL + 'apiKey=' + self.API_KEY + '&pageSize=100'
		r = requests.get(url)
		resp = json.loads(r.content.decode())
		if ['status'] == 'error':
			ret['result'] = 'failure'
			return ret
		#print(str(resp))
		totalResults = resp['totalResults']
		for i in range(1, min(11, (totalResults // 100) + 2)): # range(1, 11)
			page_url = url + '&page=' + str(i)
			r = requests.get(page_url)
			resp2 = json.loads(r.content.decode())
			resp = resp2['articles']

			for each_article in resp:
				article = {}
				article['title'] = each_article['title']
				article['source']= each_article['source']['name']
				article['content'] = each_article['content']
				article['link'] = each_article['url']
				article['date'] = each_article['publishedAt']
				article['keywords'] = [a for a in article['content'].split()]
				ret['articles'].append(article)
		return ret

	# Gets all articles based on a list of keywords
	def get_allArticles(self, keywords):
		ret = {"result": "success"}
		ret['articles'] = []

		for title in self.articles_title:
			ret['articles'].append(self.articles_title[title])

		for keyword in keywords:
			url = self.URL + 'q="' + keyword.replace(' ','%20').replace('"', '') + '"&apiKey=' + self.API_KEY + '&pageSize=100'
			r = requests.get(url)
			resp = json.loads(r.content.decode())
			if ['status'] == 'error':
				continue
			totalResults = resp['totalResults']
			for i in range(1, min(11, (totalResults // 100) + 2)): # range(1, 11)
				page_url = url + '&page=' + str(i)
				r = requests.get(page_url)
				resp2 = json.loads(r.content.decode())
				resp = resp2['articles']

				for each_article in resp:
					article = {}
					article['title'] = each_article['title']
					article['source']= each_article['source']['name']
					article['content'] = each_article['content']
					article['link'] = each_article['url']
					article['date'] = each_article['publishedAt']
					article['keywords'] = []
					ret['articles'].append(article)
		return ret

	# Puts a user uploaded article into the dictionaries
	def put_userArticle_title(self, article):
		title = article['title']
		source = article['source']
		keywords = article['keywords']

		self.articles_title[title] = article

		self.articles_source[source] = article

#		self.articles_keyword[keywords] = article



	# Puts a list of user articles into the dictionaries containing them
	def post_userArticles(self, articles):
		for article in articles:
			self.put_userArticle_title(article)

	# Deletes a user article from the dictionaries based in its title
	def delete_userArticle(self, titleToDelete):
		newTitle = {}
		newSource = {}
		newKeyword = {}
		for title in self.articles_title:
			for article in self.articles_title[title]:
				if article['title'] == titleToDelete:
					pass
				else:
					if title not in newTitle:
						newTitle[title] = []
					newTitle[title].append(article)
		for source in self.articles_source:
			for article in self.articles_source[source]:
				if article['title'] == titleToDelete:
					pass
				else:
					if source not in newSource:
						newSource[source] = []
					newSource[source].append(article)
		for keyword in self.articles_keyword:
			for article in self.articles_keyword[keyword]:
				if article['title'] == titleToDelete:
					pass
				else:
					if keyword not in newKeyword:
						newSource[keyword] = []
					newSource[keyword].append(article)


		self.articles_title = newTitle # based on title
		self.articles_source = newSource # based on source
		self.articles_keyword = newKeyword # based on key word

	# Deletes all user uploaded articles
	def delete_all_userArticles(self):
		self.articles_title = {} # based on title
		self.articles_source = {} # based on source
		self.articles_keyword = {} # based on key word

	# Generates an article in the proper format
	def makeArticle(self, title, source, link, content, date, keywords=None):
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
