import cherrypy
from helpers import *
from mako.lookup import TemplateLookup


class IradsAnalysis(object):

    database = None
    lookup = TemplateLookup(directories=['templates'])

    def __init__(self, database):
        self.database = database

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def index(self):
        template = self.lookup.get_template('analysis/analysis.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)
