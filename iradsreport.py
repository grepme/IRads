import cherrypy
from database.mappings import *
from helpers import *
from mako.lookup import TemplateLookup


class IradsReport(object):

    """Responsible for producing a list of all patients with a specified
    diagnosis for a given time period.
    """

    database = None
    lookup = TemplateLookup(directories=['templates'])

    def __init__(self, database):
        self.database = database

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def index(self):
        """Returns the main page that allows for the input of
        the parameters the user wants to search by.
        """
        template = self.lookup.get_template('report/report.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def search(self, start=None, end=None, diagnosis=None):
        """Validates the parameters, search the database, and
        returns the results or an error message page.
        """
        template = self.lookup.get_template('report/results.mako')
        (u, c) = getUserInfo()
        if start and end and diagnosis:
            diagnosis = escape(diagnosis, True)
            session = self.database.get()
            results = []
            # TODO split keyword to work with multiple words
            for entry in session.query(
                RadiologyRecord).filter(
                    RadiologyRecord.test_date >= start,
                    RadiologyRecord.test_date <= end,
                    RadiologyRecord.diagnosis.ilike(
                        "%" + diagnosis + "%")).all():
                results.append(
                    [entry.patient.last_name, entry.patient.first_name,
                     entry.patient.address, entry.patient.phone,
                     entry.test_date, entry.diagnosis])
            if (len(results) == 0):
                template = self.lookup.get_template('report/report.mako')
                return template.render(username=u, classtype=c, action="fail")
            return template.render(username=u, classtype=c, results=results)
        else:
            return template.render(username=u, classtype=c, action="noparams")
