# Hot News
# Katherine Hecht, Richard Stefanik, Jack Hill
# articles.py
# 12/2/18
import re, json
import cherrypy
from _article_database import _article_database

class ArticleController(object):
	# initialize database
	def __init__(self, adb=None):
		if adb is None:
			self.adb = _article_database()
		else:
			self.adb = adb

	# get a single article by specified title
	# format: /userArticles/:title
	def GET_USER_TITLE(self, title):
		output = {'result' : 'success'}
		output['article'] = {}
		article = self.adb.get_userArticle(title)
		if article is not None:
			output['article']['title'] = title
			output['article']['source'] = article['source']
			output['article']['keywords'] = article['keywords']
			output['article']['content'] = article['content']
			output['article']['link'] = article['link']
			output['article']['date'] = article['date']

		else:
			output['result'] = 'error'
			output['message'] = 'article not found'

		return json.dumps(output)

	# gets all user articles
	# format: /userArticles
	def GET_USER_ALL(self):
		output = {'result' : 'success'}
		output['articles'] = []
		articles = self.adb.get_all_userArticles()
		if articles is not None:
			output['articles'] = articles
		else:
			output['result'] = 'error'

		return json.dumps(output)

	# get news article by source
	# format: /newsArticles/:source
	def GET_NEWS_SRC(self, source):
		output = {'result' : 'success'}
		output['articles'] = []
		news = self.adb.get_newsArticle_source(source)
		if news['result'] == 'success':
			output['articles'] = news['articles']
		else:
			output['result'] = 'error'

		return json.dumps(output)

	#/newsArticles/:keywords/:source
	def GET_NEWS_KEY_SRC(self, keywords, source):
		output = {'result' : 'success'}
		keywords = keywords.split('||')
		output['articles'] = []
		all_news = self.adb.get_newsArticle_keyword_and_source(keywords, source)
		if all_news['result'] == 'success':
			output['articles'] = all_news['articles']
		else:
			output['result'] = 'error'

		return json.dumps(output)

	# get all articles with specified keywords
	# format: /allArticles/:keywords
	def GET_ALL_ARTICLES_K(self, keywords):
		output = {'result' : 'success'}
		keywords = keywords.split('||')
		output['articles'] = []
		all_articles = self.adb.get_allArticles(keywords)
		if all_articles['result'] == 'success':
			output['articles'] = all_articles['articles']
		else:
			output['result'] = 'error'

		return json.dumps(output)

	# get state information formatted as a dictionary with the key of date
	# format: /stateInfo/:keywords/:type
	def GET_STATE_KEY_TYPE(self, keywords, type, startDay, daysPrev):
		output = {'result' : 'success'}
		keywords = keywords.split('||')
		output['dates'] = {}
		allDates = self.adb.get_stateInfo_range(keywords, startDay, int(daysPrev), type)
		try:
			output['dates'] = allDates['dates']
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)

		print("In Get_state\noutput:")
		print(output)
		
		return json.dumps(output)

	# uploading a user article by title
	# format: /userArticles/:title
	def PUT_USER_TITLE(self, title): 	
		output = {'result' : 'success'}
		data = json.loads(cherrypy.request.body.read())
		data['title'] = title
		try:
			self.adb.put_userArticle_title(data)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)

		return json.dumps(output)

	# posting userArticles
	# format: /userArticles
	def POST(self):
		output = {'result' : 'success'}
		data = json.loads(cherrypy.request.body.read())
		try:
			self.adb.post_userArticles(data)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)

		return json.dumps(output)

	# delete an article by given title
	# format: /userArticles/:title
	def DELETE_TITLE(self, title):
		output = {'result' : 'success'}
		try:
			self.adb.delete_userArticle(title)
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)

		return json.dumps(output)

	# delete all userArticles from the database
	# format: /userArticles
	def DELETE_ALL(self):
		output = {'result' : 'success'}
		try:
			self.adb.delete_all_userArticles()
		except Exception as ex:
			output['result'] = 'error'
			output['message'] = str(ex)

		return json.dumps(output)
