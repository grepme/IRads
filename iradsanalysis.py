import cherrypy
from database.database import Database
from database.mappings import *
from helpers import *
from mako.lookup import TemplateLookup


class IradsAnalysis(object):

    """Responsible for the data analysis module."""

    lookup = TemplateLookup(directories=['templates'])

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def index(self):
        """Returns the main page of the module
        which allows a user to generate a report for analysis,
        based on specified criteria.
        """
        template = self.lookup.get_template('analysis/analysis.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)
