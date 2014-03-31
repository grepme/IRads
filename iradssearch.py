import base64
import cherrypy
from database.database import Database
from database.mappings import *
from helpers import *
from mako.lookup import TemplateLookup
from sqlalchemy import desc, or_


class IradsSearch(object):

    """Responsible for searching the database for relevant radiology
    records based on search paramenters and user's class security level.
    """

    lookup = TemplateLookup(directories=['templates'])

    @cherrypy.expose
    @cherrypy.tools.protect()
    def index(self):
        """Returns the main page that allows for the input of
        the parameters the user wants to search by.
        """
        template = self.lookup.get_template('search/search.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect()
    def search(self, start=None, end=None, keywords=None, sort=None):
        """Validates the parameters, search the database, and
        returns the results or an error message page.
        """
        template = self.lookup.get_template('search/search_results.mako')
        (u, c) = getUserInfo()
        if not ((start and end and sort) or (keywords and sort)):
            template = self.lookup.get_template('search/search.mako')
            return template.render(username=u, classtype=c, action="noparams")
        conn = Database()
        session = conn.get()
        user = session.query(User).filter(User.user_name == u).one()
        query = session.query(RadiologyRecord)
        # Check if a date has been passed
        if (start and end):
            query = query.filter(RadiologyRecord.test_date >= start,
                                 RadiologyRecord.test_date <= end)
        # Check user's security level
        if (c == 'd'):
            '''
            Checks that both the record's doctor id is the same as the
            current user's id and that the user's id is in the family_doctor
            table for the record's patient id
            '''
            query = query.join(
                FamilyDoctor, FamilyDoctor.doctor_id == user.person_id).filter(
                    RadiologyRecord.doctor_id == user.person_id).filter(
                        FamilyDoctor.patient_id == RadiologyRecord.patient_id)
        elif (c == 'r'):
            query = query.filter(
                RadiologyRecord.radiologist_id == user.person_id)
        elif (c == 'p'):
            query = query.filter(
                RadiologyRecord.patient_id == user.person_id)
        # Checks sort type
        if (sort == 'newest'):
            query = query.order_by(desc(RadiologyRecord.test_date))
        elif (sort == 'oldest'):
            query = query.order_by(RadiologyRecord.test_date)
        else:
            query = query
        if (keywords):
            '''
            Split keywords into separate words and search for each word
            as a keyword instead of the whole keyword as one string
            '''
            query = query.join(
                Person, RadiologyRecord.patient_id == Person.person_id)
            for word in keywords.split():
                query = query.filter(or_(
                    Person.last_name.ilike("%"+word+"%"),
                    Person.first_name.ilike("%"+word+"%"),
                    RadiologyRecord.diagnosis.ilike("%"+word+"%"),
                    RadiologyRecord.description.ilike("%"+word+"%")))
        results = []
        for entry in query.all():
                # Build a dict to the structure that the template expects
                current = {}
                current['id'] = entry.record_id
                current['patient_name'] = entry.patient.last_name + \
                    ", " + entry.patient.first_name
                current['doctor_name'] = entry.doctor.last_name + \
                    ", " + entry.doctor.first_name
                current['radiologist_name'] = entry.radiologist.last_name + \
                    ", " + entry.radiologist.first_name
                current['test_type'] = entry.test_type
                current['prescribing_date'] = entry.prescribing_date
                current['test_date'] = entry.test_date
                current['diagnosis'] = entry.diagnosis
                current['description'] = entry.description
                current['images'] = []
                if (len(entry.pacsimage) > 0):
                    for image in entry.pacsimage:
                        current['images'].append(
                            [image.image_id,
                                base64.b64encode(image.thumbnail),
                                base64.b64encode(image.regular_size),
                                base64.b64encode(image.full_size)])
                results.append(current)
        if (len(results) > 0):
            conn.close()
            return template.render(username=u, classtype=c, results=results)
        else:
            conn.close()
            template = self.lookup.get_template('search/search.mako')
            return template.render(username=u, classtype=c, action="fail")
