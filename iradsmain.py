import cherrypy
import os.path
from config import *
from mako.template import Template
from mako.lookup import TemplateLookup

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

    config = {'/': {'tools.staticdir.root': current_dir}, '/css':
             {'tools.staticdir.on': True, 'tools.staticdir.dir': 'css'}}

    Mapping = Irads()
    Mapping.analysis = IradsAnalysis()
    Mapping.manager = IradsManager()
    Mapping.report = IradsReport()
    Mapping.search = IradsSearch()
    Mapping.upload = IradsUpload()

    # Plug it into the quickstart with the default config.
    cherrypy.quickstart(Mapping, '/', config=config)
