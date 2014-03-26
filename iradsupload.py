import cherrypy
from helpers import *
from io import BytesIO
from mako.lookup import TemplateLookup
from operator import itemgetter
from PIL import Image


class IradsUpload(object):

    database = None
    lookup = TemplateLookup(directories=['templates'])

    def __init__(self, database):
        self.database = database

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['r'])
    def index(self):
        template = self.lookup.get_template('upload/upload.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['r'])
    def selectRecord(self):
        global database
        template = self.lookup.get_template('upload/selectrecord.mako')
        (u, c) = getUserInfo()
        session = self.database.get()
        user = session.query(User).filter(User.user_name == u).one()
        records = session.query(
            Person).filter(Person.person_id == user.person_id).one(
            ).radiologyrecords_radiologist
        record = []
        for r in records:
            record.append(
                [r.record_id, r.prescribing_date, r.test_date, r.diagnosis,
                 r.description])
        return template.render(
            username=u, classtype=c, records=record)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['r'])
    def addRecord(self):
        template = self.lookup.get_template('upload/addrecord.mako')
        (u, c) = getUserInfo()
        session = self.database.get()
        patients = []
        doctors = []
        for entry in session.query(User).filter(User.class_type == 'p').all():
            if (entry.person.__dict__ not in patients):
                patients.append(entry.person.__dict__)
        for entry in session.query(User).filter(User.class_type == 'd').all():
            if (entry.person.__dict__ not in doctors):
                doctors.append(entry.person.__dict__)
        if (len(patients) == 0):
            template = self.lookup.get_template('upload/upload.mako')
            return template.render(
                username=u, classtype=c, action="noPatient")
        if (len(doctors) == 0):
            template = self.lookup.get_template('upload/upload.mako')
            return template.render(
                username=u, classtype=c, action="noDoctor")
        p = sorted(patients, key=itemgetter('last_name'))
        d = sorted(doctors, key=itemgetter('last_name'))
        return template.render(
            username=u, classtype=c, patients=p, doctors=d)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['r'])
    def postRecord(self, patient=None, doctor=None, test_type=None,
                   test_date=None, prescribing_date=None, diagnosis=None,
                   description=None):
        template = self.lookup.get_template('upload/upload.mako')
        (u, c) = getUserInfo()
        if (patient and doctor and test_type and test_date and prescribing_date
                and diagnosis and description):
            session = self.database.get()
            radiologist = session.query(User).filter(User.user_name == u).one()
            record = RadiologyRecord(
                patient_id=patient, doctor_id=doctor,
                radiologist_id=radiologist.person_id, test_type=test_type,
                test_date=test_date, prescribing_date=prescribing_date,
                diagnosis=diagnosis, description=description)
            session.add(record)
            session.commit()
            return template.render(username=u, classtype=c, action="success")
        else:
            return template.render(
                username=u, classtype=c, action="error")

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['r'])
    def selectImage(self, id):
        template = self.lookup.get_template('upload/addimage.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c, id=id)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['r'])
    def postImage(self, id=None, radiologyimage=None):
        template = self.lookup.get_template('upload/upload.mako')
        (u, c) = getUserInfo()
        if (id and radiologyimage.file):
            image = Image.open(BytesIO(radiologyimage.file.read()))
            fullstream = BytesIO()
            image.save(fullstream, "JPEG")
            normalstream = BytesIO()
            normalimage = image.copy()
            normalimage.thumbnail((600, 600), Image.ANTIALIAS)
            normalimage.save(normalstream, "JPEG")
            thumbstream = BytesIO()
            thumbimage = image.copy()
            thumbimage.thumbnail((200, 200), Image.ANTIALIAS)
            thumbimage.save(thumbstream, "JPEG")
            session = self.database.get()
            pacsimage = PacsImage(
                record_id=id, thumbnail=thumbstream.getvalue(),
                regular_size=normalstream.getvalue(),
                full_size=fullstream.getvalue())
            session.add(pacsimage)
            session.commit()
            return template.render(username=u, classtype=c, action="added")
        else:
            return template.render(username=u, classtype=c, action="error")
