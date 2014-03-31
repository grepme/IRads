import cherrypy
from database.mappings import *
from helpers import *
from mako.lookup import TemplateLookup
import datetime
from Database import database

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
		
		#Database connection
		conn = Database()
		session = Database.get()
		
        # Get a list of all patients
		patients = []
        for entry in session.query(User).filter(User.class_type == 'p').all():
            if (entry.person.__dict__ not in patients):
                patients.append(entry.person.__dict__)
		
        template = self.lookup.get_template('analysis/analysis.mako')
        (u, c) = getUserInfo()
		
		conn.close()
		
        return template.render(username=u, classtype=c, patients=patients)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def generate(self, keywords, options, patient):
        """Returns a generated report for the analysis module"""
        template = self.lookup.get_template('analysis/generate.mako')
		
		#Database connection
		conn = Database()
		session = Database.get()
		
		#Today
		today = datetime.date.today()
		
		#All edge cases are inclusive
		if options != "all":
			if options == "week":
				minimalStartDate = today - datetime.date.today().weekday()
			elif options == "month":
				minimalStartDate = today - datetime.date.today().day
			elif options = "year":
				minimalStartDate = today - datetime.date.today().timetuple().tm_yday
		else:
			results = session.query(RadiologyRecord).filter(
				RadiologyRecord.test_type.ilike("%" + keywords + "%" ))
			
		(u, c) = getUserInfo()
		
		conn.close()
		
        return template.render(username=u, classtype=c, results=results)
