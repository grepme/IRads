import base64
import cherrypy
from database.mappings import *
from helpers import *
from mako.lookup import TemplateLookup
from sqlalchemy import or_


class IradsSearch(object):

    database = None
    lookup = TemplateLookup(directories=['templates'])

    def __init__(self, database):
        self.database = database

    @cherrypy.expose
    @cherrypy.tools.protect()
    def index(self):
        template = self.lookup.get_template('search/search.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect()
    def search(self, start=None, end=None, keywords=None, sort=None):
        template = self.lookup.get_template('search/search_results.mako')
        (u, c) = getUserInfo()
        if not ((start and end and sort) or (keywords and sort)):
            template = self.lookup.get_template('search/search.mako')
            return template.render(username=u, classtype=c, action="noparams")
        session = self.database.get()
        user = session.query(User).filter(User.user_name == u).one()
        query = session.query(RadiologyRecord)
        if (start and end):
            query = query.filter(RadiologyRecord.test_date >= start,
                                 RadiologyRecord.test_date <= end)
        if (c == 'd'):
            query = query.filter(
                RadiologyRecord.doctor_id == user.person_id)
        if (c == 'r'):
            query = query.filter(
                RadiologyRecord.radiologist_id == user.person_id)
        if (c == 'p'):
            query = query.filter(
                RadiologyRecord.patient_id == user.person_id)
        if (keywords):
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
                current = {}
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
                                base64.b64encode(image.thumbnail)])
                results.append(current)
        if (len(results) > 0):
            return template.render(username=u, classtype=c, results=results)
        else:
            template = self.lookup.get_template('search/search.mako')
            return template.render(username=u, classtype=c, action="fail")
