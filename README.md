# ParadigmsProject
# Jack Hill, Rick Stefanik and Katherine Hecht
# November 6, 2018

PHASES

PHASE 1:
We plan to create JSON files by crawling through different websites (cnn, nbc, fox, bbc, etc...).  
The JSON files we create will contain data on the location of where news has occurred and its content.

From this data, we plan to create a heat map that will show where news has most often occurred.
This heat map can be filtered based on the different news sites and categories of news.  
The links to the different news articles will be displayed if the user clicks on that given location.

PHASE 2:
API:
We are using the API from newsapi.org. Our API works to get information regarding news articles ranging over the past 30 days.
The base url for our API calls 'https://newsapi.org/v2/everything?' to get everything in the initial phase. 
Our goal of our project is to get the accumulated number of article 'hits' based on the user entered keywird per state over a
apecified day range. Therefore, our feature of the API involves modifying the urls to include the user specified keyword, day 
interval, and each state iterated over a for loop. This is clearly seen in our function 'get_StateInfo_keyword(). As we are using 
an API that constantly changes, we created a USER_ARTICLES functionality to test for correctness as seen below. The format of our desired
information is seen in the structure of each article in either API_ARTICLES or USER_ARTICLES to have the following format:
Article {
“Result” : “success”,
“Articles”: [
{
	“Title” : title,
	“Source” : source,
	“Keywords” : [k1, k2],
	“Link” : url,
	“Content” : content,
	“date” : publishedAt (2018-10-20T13:00:00Z)
}
	]
}

PHASE 3:
We are using port number 52071.
Our webservice should be used to see how the frequency of news topics discussed throughout the nation over time. In doing this API call,
the user can see news articles per state. For example, the user can select the keyword 'election', day November 27, 2018(2018-11-27), the 
number of days the user wants to see previous to the day selected. Once selecting 'search', the user will be prompted with a heat map of
the United States and may click on a colored state to see the total number of articles and further navigate to one of the top five
articles shown.  For info on running and testing the server, see Test (PHASE 3) section below.

PHASE 4:
We are still using port 52071. The webservice expands upon the above functionalities. The user may now enter multiple
keywords separated by a ', '. They can then select if they want to look through user uploaded articles, the API, or both.
Further, the user can select a date to search articles by, which is checked to be in the past two weeks.
The user can also choose days previous to initial date in which they want to check. Once the user clicks 
'Search', a heat map of the United States is colored according to frecuency of articles. The user can then 
click on a state to see the top five links related to the key word. See test for phase 4 below to see how to test the client.


TESTS
Note: If you do not already have python 3.6 installed, use '/afs/nd.edu/user14/csesoft/2017-fall/anaconda3/bin/python' to run the following tests.

Test (PHASE 2):
To run our test script, run 'python3.6 test_api.py.' There are six cases that the file will test for correctness of the user file.
The first tests for getting the user article which should result in an empty dictionary. The second tests for getting all of the 
user articles which should result an empty list that would, if filled contain dictionaries. The third tests to put a user article.
Here, we see the format of the article and test based upon whether the article at "fake title 1" is properly added. The fourth tests
posting asticles with two fake sorces which should return the two articles back. The fifth deletes a specific article by comparing the deleted
value to an empty dictionary to prove correctness. The sixth tests for getting the accumulated state information for a given day. 

Test (PHASE 3):
To start the server, run 'python3.6 main.py'. While this is running, you can use the command 'python3.6 test_ws.py' to execute our tests for the
cherrypy web server. Two of the tests are testing GET, one gets all user uploaded articles and the other gets one user uploaded article
specified by title. After that, we have a PUT test that tests putting a single user article into the database, and also a POST test that tests
inserting a list of user articles into the database. We also have 2 DELETE tests, one that tests deleting all user uploaded articles from the
databse and one testing just deleting a single article based on its title. Lastly, we have a test that checks our GET method that gets a dictionary
of dates, where each date has a dictionary of all states and the number of articles that are related to that state, along with up to 5 links to
articles from that state.

Test (PHASE 4):
Follow steps from the phase 3 test to start the server, and then navigate to the client at 'http://student04.cse.nd.edu/khecht/paradigms/floodFill.html'.
You can now enter a keyword below the map, for example type in 'football'. Select 'News Sites' as the source and decide a date (within the last 2 weeks)
and a range of days previous to look for articles in. Click submit and you will have to wait while the API calls are executed and then the heat
map will be generated. You can switch which day you are looking at on the map using the slider above the map. If you want to upload your own article
and/or look at other user articles, use the nav bar at the top and click on either 'Content Management' and 'View Articles'. When selecting 
'View Articles', the user can enter the title of the article they want to search by and whether they want to look for a single article or all articles. 
When selecting 'Content Management', the user can add articles, view articles, and delete articles using the client. If you are going to upload 
multiple articles, you can add each one to a queue and then upload all of the articles at once.Once you have uploaded articles, you can check out 
how they affect the heat map by going back and changing the source for the map to 'Uploaded Content'. If you want to use uploaded content alongside 
news sites you can select 'Both'. Checks are in place for which dates a user can choose, and an error message should be displayed if an invalid one 
is chosen. Since we are using the free version of the API, we only have access to a limited time frame to get articles from.
