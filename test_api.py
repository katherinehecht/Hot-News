#! /usr/bin/env python3
from _article_database import _article_database
import unittest
import json

class TestArticleDatabase(unittest.TestCase):
    """unit tests for python primer homework"""

    #@classmethod
    #def setUpClass(self):
    adb = _article_database()

    def reset_data(self):
        "reset data is required because we cannot promise an order of test case execution"
        self.adb.delete_all_userArticles()

    def test_get_userarticle(self):
        self.reset_data()
        ret = self.adb.get_userArticle("Fake title")
        self.assertEqual(ret, {})

    def test_get_all_userArticles(self):
        self.reset_data()
        ret = self.adb.get_all_userArticles()
        self.assertEqual(ret, [])

    def test_put_userArticle_title(self):
        self.reset_data()
        article = {
            "title" : "fake title 1",
            "source" : "fake source 1",
            "keywords" : ["fake key 1", "fake key 2"],
            "link" : "https://fakelink.com",
            "content" : "this is all a test",
            "date" : "2018-10-20T13:00:00Z"
        }
        self.adb.put_userArticle_title(article)
        ret = self.adb.get_userArticle("fake title 1")
        self.assertEqual([article], ret)

    def test_post_userArticles(self):
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
        self.adb.post_userArticle(articles)
        ret = self.adb.get_all_userArticles()
        self.assertEqual(ret, articles)

    def test_delete_userArticle(self):
        self.reset_data()
        article = {
            "title" : "fake title 1",
            "source" : "fake source 1",
            "keywords" : ["fake key 1", "fake key 2"],
            "link" : "https://fakelink.com",
            "content" : "this is all a test",
            "date" : "2018-10-20T13:00:00Z"
        }
        self.adb.put_userArticle_title(article)
        ret = self.adb.delete_userArticle("fake title 1")
        ret = self.adb.get_userArticle("fake title 1")
        self.assertEqual({}, ret)

    def test_delete_all_userArticle(self):
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
        self.adb.post_userArticle(articles)
        self.adb.delete_all_userArticles()
        ret = self.adb.get_all_userArticles()
        self.assertEqual([], ret)

    def test_get_stateInfo_range(self):
        self.reset_data()
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
        }
        ]
        self.adb.post_userArticle(articles)
        ret = self.adb.get_stateInfo_range(["politics", "election"], "2018-11-05", 2, "USER")
        self.assertEqual(ret['dates']["2018-11-05"]["California"]["value"], 1)
        self.assertEqual(ret['dates']["2018-11-04"]["New York"]["value"], 1)
        self.assertEqual(ret['dates']["2018-11-04"]["California"]["value"], 0)
        self.assertEqual(ret['dates']["2018-11-05"]["New York"]["value"], 0)

    def test_api_data(self):
        self.reset_data()
        with open("api_data.json", "r") as f:
            data = json.load(f)
        articles = data["articles"]
        self.adb.post_userArticle(articles)
        ret = self.adb.get_stateInfo_range(["election"], "2018-11-07", 1, "USER")
        self.assertEqual(1, ret['dates']["2018-11-07"]["New York"]["value"])


if __name__ == "__main__":
    unittest.main()
