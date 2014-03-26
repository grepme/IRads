import cherrypy
from database.mappings import *
from helpers import *
from mako.lookup import TemplateLookup


class IradsReport(object):

    database = None
    lookup = TemplateLookup(directories=['templates'])

    def __init__(self, database):
        self.database = database

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def index(self):
        template = self.lookup.get_template('report/report.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def search(self, start=None, end=None, diagnosis=None):
        template = self.lookup.get_template('report/results.mako')
        (u, c) = getUserInfo()
        if start and end and diagnosis:
            diagnosis = escape(diagnosis, True)
            session = self.database.get()
            results = []
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
