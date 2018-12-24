# Hot News
# Katherine Hecht, Richard Stefanik, Jack Hill
# main.py
# 12/2/18
import cherrypy
import json
from articles import ArticleController

class optionsController(object):
	def OPTIONS(self, *args, **kargs):
		return ""

# define CORS and options
def CORS():
	cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
	cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
	cherrypy.response.headers["Access-Control-Allow-Credentials"] = "*"


def start_service():
	# object of controller
    articleController = ArticleController()

	# create dispatcher
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    # GET functions
    dispatcher.connect('get_user_articles_by_title', '/userArticles/:title', controller = articleController, action='GET_USER_TITLE', conditions=dict(method = ['GET']))
    dispatcher.connect('get_all_user_articles', '/userArticles/', controller = articleController, action='GET_USER_ALL', conditions=dict(method = ['GET']))
    dispatcher.connect('get_state_key_type', '/stateInfo/:keywords/:type/:startDay/:daysPrev', controller = articleController, action='GET_STATE_KEY_TYPE', conditions=dict(method = ['GET']))

    # PUT functions
    dispatcher.connect('put_user_article_title', '/userArticles/:title', controller = articleController, action='PUT_USER_TITLE', conditions=dict(method = ['PUT']))

    # POST functions
    dispatcher.connect('post_user_articles', '/userArticles/', controller = articleController, action='POST', conditions=dict(method = ['POST']))

    # DELETE functions
    dispatcher.connect('delete_user_article', '/userArticles/:title', controller = articleController, action='DELETE_TITLE', conditions=dict(method = ['DELETE']))
    dispatcher.connect('delete_all_user_articles', '/userArticles/', controller = articleController, action='DELETE_ALL', conditions=dict(method = ['DELETE']))

    # OPTIONS functions
    dispatcher.connect('states_options', '/stateInfo/:keywords/:type/:startDay/:daysPrev', controller = optionsController, action='OPTIONS', conditions=dict(method = ['OPTIONS']))
    dispatcher.connect('get_all', '/userArticles/:title', controller = optionsController, action='OPTIONS', conditions=dict(method = ['OPTIONS']))
    dispatcher.connect('get_title', '/userArticles/', controller = optionsController, action='OPTIONS', conditions=dict(method = ['OPTIONS']))
    dispatcher.connect('put_title', '/userArticles/:title', controller = optionsController, action='OPTIONS', conditions=dict(method = ['OPTIONS']))
    dispatcher.connect('post', '/userArticles/', controller = optionsController, action='OPTIONS', conditions=dict(method = ['OPTIONS']))
    dispatcher.connect('delete_title', '/userArticles/:title', controller = optionsController, action='OPTIONS', conditions=dict(method = ['OPTIONS']))
    dispatcher.connect('delete_all', '/userArticles/', controller = optionsController, action='OPTIONS', conditions=dict(method = ['OPTIONS']))

	# configuration for server
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

	# update config
    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)

if __name__ == '__main__':
	# enable CORS
	cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
	# begin main functionality
	start_service()
