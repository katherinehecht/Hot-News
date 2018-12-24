# Katherine Hecht, Richard Stefanik, Jack Hill
# test_ws.py
# This is a test file for milestone 3 of the final project. 
from _article_database import _article_database
import unittest
import json
import requests

class TestArticleDatabase(unittest.TestCase):
	# initialize database and URL
	adb = _article_database()
	URL = 'http://student04.cse.nd.edu:52071'
	
	# reset the articles data
	def reset_data(self):
		a = []
		r = requests.put(self.URL + '/userArticles', data = json.dumps(a))
	
	# test getting the article via the stateInfo URL
	def test_get_state_key_type(self):
		self.reset_data()
		# initialize two fake articles to post
		articles = [
		        {
				"title" : "fake title 6",
				"source" : "fake source 6",
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
				},
		
			]
		# post the two articles
		r = requests.post(self.URL + '/userArticles', data=json.dumps(articles))
		resp = json.loads(r.content.decode())
		
		# get request with specified parameters 
		# url is structured /stateInfo/:keywords/:type/:date/:daysPrev
		r = requests.get(self.URL + '/stateInfo/politics/USER/2018-11-05/2')
		resp = json.loads(r.content.decode())
		
		# test values for articles against the response queried from the get
		self.assertEqual(resp['dates']["2018-11-05"]["California"]["value"], 1)
		self.assertEqual(resp['dates']["2018-11-04"]["New York"]["value"], 1)
		self.assertEqual(resp['dates']["2018-11-04"]["California"]["value"], 0)
		self.assertEqual(resp['dates']["2018-11-05"]["New York"]["value"], 0)
	
	# tests the putting and getting of an article specified by title
	def test_get_and_put_userArticle_title(self):
		self.reset_data()
		# initialize title and article for test
		title = "faketitle1"
		article = {
        	    "source" : "fake source 1",
        	    "keywords" : ["fake key 1", "fake key 2"],
        	    "link" : "https://fakelink.com",
        	    "content" : "this is all a test",
        	    "date" : "2018-10-20T13:00:00Z"
        	}

		# put request
		r = requests.put(self.URL + '/userArticles/' + title, data=json.dumps(article))
		resp = json.loads(r.content.decode('utf-8'))
		self.assertEqual(resp['result'], 'success')
		
		# get request to test 
		r = requests.get(self.URL + '/userArticles/' + title)
		resp = json.loads(r.content.decode('utf-8'))
		article['title'] = title # add title component to article
		self.assertEqual(article, resp['article']) 

	# tests posting of two articles and getting of all articles
	def test_post_and_get_all_userArticles(self):
		self.reset_data()
		# initialize articles 
		articles = [
				{
					"title" : "fake title 2",
					"source" : "fake source 2",
					"keywords" : ["fake key 3", "fake key 4"],
					"link" : "https://fakelink2.com",
					"content" : "this is testing post",
					"date" : "2018-10-10T18:00:00Z"
					},
				{
					"title" : "fake title 3",
					"source" : "fake source 3",
					"keywords" : ["fake key 5", "fake key 6"],
					"link" : "https://fakelink.com",
					"content" : "this is testing post",
					"date" : "2018-10-20T13:00:00Z"
				}
				]
		# post request for two articles
		r = requests.post(self.URL + '/userArticles', data=json.dumps(articles))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'], 'success')

		# get all request
		r = requests.get(self.URL + '/userArticles')
		resp = json.loads(r.content.decode())
		article_list = resp['articles']
		# loop through the articles from get
		for article in article_list:
			# compare to find a matched title
			if article['title'] == "fake title 2":
				# if matched title, check if article data is equivalent
				self.assertEqual(article, articles[0])
	
	# tests deletion of an article specified by title from userArticles
	def test_delete_title(self):
		self.reset_data()
		articles = [
				{
					"title" : "faketitle2",
					"source" : "fake source 2",
					"keywords" : ["fake key 3", "fake key 4"],
					"link" : "https://fakelink2.com",
					"content" : "this is testing post",
					"date" : "2018-10-10T18:00:00Z"
					},
				{
					"title" : "faketitle3",
					"source" : "fake source 3",
					"keywords" : ["fake key 5", "fake key 6"],
					"link" : "https://fakelink.com",
					"content" : "this is testing post",
					"date" : "2018-10-20T13:00:00Z"
				}
				]
		# post request for two articles
		r = requests.post(self.URL + '/userArticles', data=json.dumps(articles))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'], 'success')
		
		# delete the first article with title "fake title 2"
		title = "faketitle2"
		r = requests.delete(self.URL + '/userArticles/' + title)
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'], 'success')
		
		# attempt to get article "faketitle2"
		r = requests.get(self.URL + '/userArticles/' + title)
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'], 'error')

	# tests deletion of all articles from userArticles
	def test_delete_all(self):
		self.reset_data()
		articles = [
				{
					"title" : "fake title 2",
					"source" : "fake source 2",
					"keywords" : ["fake key 3", "fake key 4"],
					"link" : "https://fakelink2.com",
					"content" : "this is testing post",
					"date" : "2018-10-10T18:00:00Z"
					},
				{
					"title" : "fake title 3",
					"source" : "fake source 3",
					"keywords" : ["fake key 5", "fake key 6"],
					"link" : "https://fakelink.com",
					"content" : "this is testing post",
					"date" : "2018-10-20T13:00:00Z"
				}
				]
		# post request for two articles
		r = requests.post(self.URL + '/userArticles', data = json.dumps(articles))
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'], 'success')

		# delete all articles from userArticles
		r = requests.delete(self.URL + '/userArticles')
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['result'], 'success')
		
		# get all articles and compare against empty list for correctness 
		r = requests.get(self.URL + '/userArticles')
		resp = json.loads(r.content.decode())
		self.assertEqual(resp['articles'], [])

if __name__ == "__main__":
    unittest.main()
