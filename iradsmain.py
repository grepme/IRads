import cherrypy
import os.path
from authentication import *
from config import *
from mako.lookup import TemplateLookup
from database.database import Database

lookup = TemplateLookup(directories=['templates'])


class Irads(object):

    @cherrypy.expose
    def index(self):
        template = lookup.get_template('login.mako')
        return template.render()

    @cherrypy.expose
    def home(self):
        template = lookup.get_template('home.mako')
        return template.render()


class IradsAnalysis(object):

    @cherrypy.expose
    def index(self):
        template = lookup.get_template('analysis/analysis.mako')
        return template.render()


class IradsManager(object):

    @cherrypy.expose
    def index(self):
        template = lookup.get_template('manager/manager.mako')
        return template.render()


class IradsReport(object):

    @cherrypy.expose
    def index(self):
        template = lookup.get_template('report/report.mako')
        return template.render()


class IradsSearch(object):

    @cherrypy.expose
    def index(self):
        template = lookup.get_template('search/search.mako')
        return template.render()


class IradsUpload(object):

    @cherrypy.expose
    def index(self):
        template = lookup.get_template('upload/upload.mako')
        return template.render()


if (__name__ == '__main__'):
    current_dir = os.path.dirname(os.path.abspath(__file__))

    config = {'/': {'tools.staticdir.root': current_dir,
                    'tools.sessions.on': True,
                    'tools.sessions.storage_type': "ram",
                    'tools.sessions.timeout': 3600
                    },
              '/css':
             {'tools.staticdir.on': True, 'tools.staticdir.dir': 'css'}}

    Mapping = Irads()
    Mapping.analysis = IradsAnalysis()
    Mapping.manager = IradsManager()
    Mapping.report = IradsReport()
    Mapping.search = IradsSearch()
    Mapping.upload = IradsUpload()
	
	#Connect to the database
	database = Database(connect=True)
	database.connect(DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOSTNAME, DATABASE)
	

    # Plug it into the quickstart with the default config.
    cherrypy.quickstart(Mapping, '/', config=config)
