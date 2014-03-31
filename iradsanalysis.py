import cherrypy
from database.database import Database
from database.mappings import *
from sqlalchemy import func, distinct
from helpers import *
from mako.lookup import TemplateLookup
import datetime


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

        # Database connection
        conn = Database()
        session = conn.get()

        # Get a list of all patients
        patients = []
		testTypes = []
        for entry in session.query(User).filter(User.class_type == 'p').all():
            if (entry.person.__dict__ not in patients):
                patients.append(entry.person.__dict__)
				
        for entry in session.query(RadiologyRecord).filter(distinct(RadiologyRecord.test_type)).all():
            if (entry.test_type not in testTypes):
                testTypes.append(entry.test_type)

        template = self.lookup.get_template('analysis/analysis.mako')
        (u, c) = getUserInfo()

        conn.close()

        return template.render(username=u, classtype=c, patients=patients, testTypes=testTypes)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def generate(self, keywords=None, options=None, patient=None, testType=None):
        """Returns a generated report for the analysis module"""
        template = self.lookup.get_template('analysis/generate.mako')

        # Database connection
        conn = Database()
        session = conn.get()

        # Today
        today = datetime.date.today()

        # All edge cases are inclusive
        if options != "all" or options is not None:
            if options == "week":
                minimalStartDate = today - datetime.date.today().weekday()
            elif options == "month":
                minimalStartDate = today - datetime.date.today().day
            elif options == "year":
                minimalStartDate = today - \
                    datetime.timedelata(days=datetime.date.today().timetuple().tm_yday + 1)
			
			results = session.query(func.count(RadiologyRecord.pacsimage) ,RadiologyRecord).filter( \
			minimalStartDate <= RadiologyRecord.test_date <= today).ilike("%" + keywords + "%")).all()
			
        else:
            results = session.query(RadiologyRecord).filter(
                RadiologyRecord.test_type.ilike("%" + keywords + "%"))

        (u, c) = getUserInfo()

        conn.close()

        return template.render(username=u, classtype=c, results=results)
