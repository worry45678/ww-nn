from tornado.options import options, define, parse_command_line  
import tornado.httpserver  
import tornado.ioloop  
import tornado.web  
import tornado.wsgi  
import os, sys  
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from manage import app
from bokeh.util.browser import view
#SITE_ROOT = os.path.dirname(os.getcwd())   
#PROJECT_NAME = os.path.basename(os.getcwd())  
  
#sys.path.append( SITE_ROOT )  
  
define('port', type=int, default=8080)  
def main():  
    tornado.options.parse_command_line()  

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(options.port)
    #tornado.ioloop.IOLoop.add_callback(view, "http://localhost:%s/" % options.port)
    tornado.ioloop.IOLoop.instance().start()  
  
if __name__ == '__main__':  
        main()  
		



