import cherrypy
from database.database import Database
from database.mappings import *
from sqlalchemy import func
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

        return template.render(
            username=u, classtype=c, patients=patients, testTypes=testTypes)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def generate(self, start=None, end=None, patient=None, testType=None):
        """Returns a generated report for the analysis module"""
        template = self.lookup.get_template('analysis/generate.mako')

        # Database connection
        conn = Database()
        session = conn.get()

        #Basic query
        #query = session.query(RadiologyRecord).join(PacsImage, RadiologyRecord.record_id == PacsImage.record_id).join(Person, RadiologyRecord.patient_id == Person.person_id)
        query = session.query(RadiologyRecord, func.count(PacsImage.record_id).label('total')).join(PacsImage).group_by(RadiologyRecord).order_by('total DESC')
        # All edge cases are inclusive
        #if (start is not None) and (end is not None):
        #    query = query.filter(
        #        RadiologyRecord.test_date <= end).filter(
        #            RadiologyRecord.test_date >= start)

        if testType != "_ALLTESTTYPES_":
            query = query.filter(RadiologyRecord.test_type == testType)

        if patient != "_ALLPATIENTS_":
            query = query.join(Person).filter(RadiologyRecord.patient_id == patient)

        results = query.all()
        #results = []
        #for entry in query.all():
        #    if entry.__dict__ not in results:
        #        results.append(entry.__dict__)

        (u, c) = getUserInfo()

        conn.close()

        return template.render(username=u, classtype=c, results=results)
