import cherrypy
import os.path
from config import *
from mako.template import Template
from mako.lookup import TemplateLookup

lookup = TemplateLookup(directories=['templates'])


class Irads(object):
    # This will expose the object to the web.
    # ie. Think public vs. private definitions.

    @cherrypy.expose
    def index(self):
        template = lookup.get_template('login.mako')
        return template.render()

    # This will map the definition to '/page1'
    @cherrypy.expose
    def page1(self):
        return "This is a side page"

    # This will map the definition to '/page2/[variable1]'
    #[variable 1 being the first variable]
    @cherrypy.expose
    def page2(self, var):
        return "You sent me the variable!: " + str(var)


class Something(object):

    @cherrypy.expose
    def index(self):
        return "This should probably have an index..."

if (__name__ == '__main__'):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # This will map the object to '/'
    Mapping = Irads()

    # I can map the class to '/somethingelse' instead!
    Mapping.somethingelse = Something()

    config = {'/': {'tools.staticdir.root': current_dir,
					'tools.sessions.on': True,
					'tools.sessions.storage_type': "ram",
					'tools.sessions.timeout': 3600
					},
	         '/css':
             {'tools.staticdir.on': True, 'tools.staticdir.dir': 'css'}}

    # Plug it into the quickstart with the default config.
    cherrypy.quickstart(Mapping, '/', config=config)
