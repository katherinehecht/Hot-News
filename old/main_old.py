import cherrypy
import json
from articles import ArticleController

class optionsController(object):
	def OPTIONS(self, *args, **kargs):
		return ""

def CORS():
	cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
	cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
	cherrypy.response.headers["Access-Control-Allow-Credentials"] = "*"


def start_service():

    articleController = ArticleController()
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    # GET functions
    #working
    dispatcher.connect('get_user_articles_by_title', '/userArticles/:title', controller = articleController, action='GET_USER_TITLE', conditions=dict(method = ['GET']))
    #working
    dispatcher.connect('get_all_user_articles', '/userArticles', controller = articleController, action='GET_USER_ALL', conditions=dict(method = ['GET']))

    #dispatcher.connect('get_news_key', '/newsArticles/:keywords', controller = articleController, action='GET_NEWS_KEY', conditions=dict(method = ['GET']))
    #dispatcher.connect('get_news_source', '/newsArticles/:source', controller = articleController, action='GET_NEWS_SRC', conditions=dict(method = ['GET']))

    #working
    #dispatcher.connect('get_news_key_and_source', '/newsArticles/:keywords/:source', controller = articleController, action='GET_NEWS_KEY_SRC', conditions=dict(method = ['GET']))
    #working
    #dispatcher.connect('get_all_articles_keyword', '/allArticles/:keywords', controller = articleController, action='GET_ALL_ARTICLES_K', conditions=dict(method = ['GET']))
    #working
    dispatcher.connect('get_state_key_type', '/stateInfo/:keywords/:type/:startDay/:daysPrev', controller = articleController, action='GET_STATE_KEY_TYPE', conditions=dict(method = ['GET']))

    # PUT functions
    dispatcher.connect('put_user_article_title', '/userArticles/:title', controller = articleController, action='PUT_USER_TITLE', conditions=dict(method = ['PUT']))

    # POST functions
    dispatcher.connect('post_user_articles', '/userArticles', controller = articleController, action='POST', conditions=dict(method = ['POST']))

    # DELETE functions
    dispatcher.connect('delete_user_article', '/userArticles/:title', controller = articleController, action='DELETE_TITLE', conditions=dict(method = ['DELETE']))
    dispatcher.connect('delete_all_user_articles', '/userArticles', controller = articleController, action='DELETE_ALL', conditions=dict(method = ['DELETE']))
    
    # OPTIONS functions
    dispatcher.connect('states_options', '/stateInfo/:keywords/:type/:startDay/:daysPrev', controller = optionsController, action='OPTIONS', conditions=dict(method = ['OPTIONS']))



    conf = {
            'global' : {
                    'server.socket_host' : 'student04.cse.nd.edu',
                    'server.socket_port' : 52071,
            },
            '/' : {
		'request.dispatch' : dispatcher,
		'tools.CORS.on' : True
		}
    }

    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)

if __name__ == '__main__':
	cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
	start_service()
