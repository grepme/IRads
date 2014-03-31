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

        for entry in session.query(RadiologyRecord).distinct().all():
            if (entry.test_type not in testTypes):
                testTypes.append(entry.test_type)

        template = self.lookup.get_template('analysis/analysis.mako')
        (u, c) = getUserInfo()

        conn.close()

        return template.render(username=u, classtype=c, patients=patients, testTypes=testTypes)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def generate(self, start=None, end=None, patient=None, testType=None):
        """Returns a generated report for the analysis module"""
        template = self.lookup.get_template('analysis/generate.mako')

        # Database connection
        conn = Database()
        session = conn.get()

        # Today
        today = datetime.date.today()

		#Basic query
		query = session.query(func.count(RadiologyRecord.pacsimage) ,RadiologyRecord)
		
        # All edge cases are inclusive
        if start is not None and end is not None:
            #if options == "week":
            #    minimalStartDate = today - datetime.date.today().weekday()
            #elif options == "month":
            #    minimalStartDate = today - datetime.date.today().day
            #elif options == "year":
            #    minimalStartDate = today - \
            #        datetime.timedelata(days=datetime.date.today().timetuple().tm_yday + 1)
			query = query.filter( \
            start <= RadiologyRecord.test_date <= end)
			
		if testType != "_ALLTESTTYPES_":
			query = query.filter(RadiologyRecord.test_type == testType)
			
		if 	patient != "_ALLPATIENTS_":
			query = query.filter(RadiologyRecord.patient.person_id == patient)
	
		results = query.all()
		
        (u, c) = getUserInfo()

        conn.close()

        return template.render(username=u, classtype=c, results=results)
