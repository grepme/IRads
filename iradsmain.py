import base64
import cherrypy
import os.path
import time
from cgi import escape
from config import *
from helpers import *
from io import BytesIO
from mako.lookup import TemplateLookup
from operator import itemgetter
from PIL import Image
from database.database import Database
from database.mappings import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

database = None
lookup = TemplateLookup(directories=['templates'])


class Irads(object):

    @cherrypy.expose
    def index(self, username=None, password=None):
        global database
        template = lookup.get_template('login.mako')
        if username and password:
            username = escape(username, True)
            password = escape(password, True)
            session = database.get()
            try:
                user = session.query(User).filter(
                    User.user_name == username).filter(
                        User.password == password).one()
                cherrypy.session['username'] = user.user_name
                cherrypy.session['classtype'] = user.class_type
                raise cherrypy.HTTPRedirect("/home")
            except NoResultFound:
                return template.render(loginStatus=1)
            except MultipleResultsFound:
                return template.render(loginStatus=1)
        else:
            return template.render(loginStatus=0)

    @cherrypy.expose
    @cherrypy.tools.protect()
    def home(self):
        template = lookup.get_template('home.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect()
    def user(self, firstname=None, lastname=None,
             address=None, email=None, phone=None,
             password=None, password2=None):
        template = lookup.get_template('user.mako')
        (u, c) = getUserInfo()
        session = database.get()
        user = session.query(User).filter(User.user_name == u).one()
        fail = False
        if password or password2:
            if password == password2:
                user.password = password
            else:
                fail = True
        if firstname and not fail:
            user.person.first_name = firstname
        if lastname and not fail:
            user.person.last_name = lastname
        if address and not fail:
            user.person.address = address
        if email and not fail:
            user.person.email = email
        if phone and not fail:
            user.person.phone = phone
        if firstname or lastname or address or email or phone or password:
            if not fail:
                session.commit()
                user = session.query(User).filter(User.user_name == u).one()
        oldinfo = []
        oldinfo.append(user.person.first_name)
        oldinfo.append(user.person.last_name)
        oldinfo.append(user.person.address)
        oldinfo.append(user.person.email)
        oldinfo.append(user.person.phone)
        if firstname or lastname or address or email or phone or password:
            if fail:
                return template.render(
                    username=u, classtype=c, oldinfo=oldinfo, action="nomatch")
            else:
                return template.render(
                    username=u, classtype=c, oldinfo=oldinfo, action="success")
        else:
            return template.render(username=u, classtype=c, oldinfo=oldinfo)

    @cherrypy.expose
    def logout(self):
        cherrypy.session.delete()
        template = lookup.get_template('login.mako')
        return template.render(loginStatus=2)

    @cherrypy.expose
    def error(self):
        cherrypy.session.delete()
        template = lookup.get_template('login.mako')
        return template.render(loginStatus=3)


class IradsAnalysis(object):

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def index(self):
        template = lookup.get_template('analysis/analysis.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)


class IradsManager(object):

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def index(self):
        template = lookup.get_template('manager/manager.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def addPerson(self, firstname=None, lastname=None,
                  address=None, email=None, phone=None):
        template = lookup.get_template('manager/addperson.mako')
        (u, c) = getUserInfo()
        if firstname:
            session = database.get()
            person = Person(
                first_name=firstname, last_name=lastname,
                address=address, email=email, phone=phone)
            session.add(person)
            session.commit()
            return template.render(username=u, classtype=c, action=True)
        else:
            return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def editPerson(self, id, firstname=None, lastname=None,
                   address=None, email=None, phone=None):
        template = lookup.get_template('manager/editperson.mako')
        (u, c) = getUserInfo()
        session = database.get()
        person = session.query(Person).filter(Person.person_id == id).one()
        if firstname:
            person.first_name = firstname
        if lastname:
            person.last_name = lastname
        if address:
            person.address = address
        if email:
            person.email = email
        if phone:
            person.phone = phone
        if firstname or lastname or address or email or phone:
            session.commit()
            person = session.query(Person).filter(Person.person_id == id).one()
            return template.render(
                username=u, classtype=c, person=person.__dict__, action=True)
        else:
            return template.render(
                username=u, classtype=c, person=person.__dict__)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def listPerson(self):
        template = lookup.get_template('manager/listperson.mako')
        (u, c) = getUserInfo()
        session = database.get()
        persons = []
        for entry in session.query(Person).order_by(Person.last_name).all():
            persons.append(entry.__dict__)
        return template.render(username=u, classtype=c, persons=persons)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def addUser(self, preset, username=None,
                password=None, classtype=None, id=None):
        template = lookup.get_template('manager/adduser.mako')
        (u, c) = getUserInfo()
        session = database.get()
        persons = []
        for entry in session.query(Person).order_by(Person.last_name).all():
            persons.append(
                [entry.person_id, entry.first_name, entry.last_name])
        if username:
            try:
                date = time.strftime("%Y-%m-%d")
                user = User(user_name=username, password=password,
                            class_type=classtype, person_id=id,
                            date_registered=date)
                session.add(user)
                session.commit()
                return template.render(
                    username=u, classtype=c, persons=persons,
                    preset=int(preset), action="success")
            except IntegrityError:
                return template.render(
                    username=u, classtype=c, persons=persons,
                    preset=int(preset), action="exists")
        else:
            return template.render(
                username=u, classtype=c, persons=persons, preset=int(preset))

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def editUser(self, userToEdit, username=None, password=None,
                 password2=None, classtype=None):
        template = lookup.get_template('manager/edituser.mako')
        (u, c) = getUserInfo()
        session = database.get()
        user = session.query(User).filter(User.user_name == userToEdit).one()
        fail = False
        if password or password2:
            if password == password2:
                user.password = password
            else:
                fail = True
        if username and not fail:
            user.user_name = username
        if classtype and not fail:
            user.class_type = classtype
        if username or password or classtype:
            if not fail:
                session.commit()
        if username or password or classtype:
            if username and not fail:
                user = session.query(User).filter(
                    User.user_name == username).one()
            else:
                user = session.query(User).filter(
                    User.user_name == userToEdit).one()
            if fail:
                return template.render(username=u, classtype=c,
                                       user=user.__dict__, action="nomatch")
            else:
                return template.render(username=u, classtype=c,
                                       user=user.__dict__, action="success")
        else:
            return template.render(
                username=u, classtype=c, user=user.__dict__)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def listUser(self):
        template = lookup.get_template('manager/listuser.mako')
        (u, c) = getUserInfo()
        session = database.get()
        users = []
        for entry in session.query(User).order_by(User.user_name).all():
            users.append(entry.__dict__)
        return template.render(username=u, classtype=c, users=users)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def listDoctor(self):
        template = lookup.get_template('manager/listdoctor.mako')
        (u, c) = getUserInfo()
        session = database.get()
        doctors = []
        for entry in session.query(
                User).filter(User.class_type == 'd').all():
            if entry.person.__dict__ not in doctors:
                doctors.append(entry.person.__dict__)
        return template.render(username=u, classtype=c, doctors=doctors)


class IradsReport(object):

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def index(self):
        template = lookup.get_template('report/report.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def search(self, start=None, end=None, diagnosis=None):
        template = lookup.get_template('report/report.mako')
        (u, c) = getUserInfo()
        if start and end and diagnosis:
            diagnosis = escape(diagnosis, True)
            session = database.get()
            results = []
            for entry in session.query(
                RadiologyRecord).filter(
                    RadiologyRecord.test_date >= start,
                    RadiologyRecord.test_date <= end,
                    RadiologyRecord.diagnosis.ilike(
                        '%' + diagnosis + '%')).all():
                results.append(
                    [entry.patient.last_name, entry.patient.first_name,
                     entry.patient.address, entry.patient.phone,
                     entry.test_date, entry.diagnosis])
                template = lookup.get_template('report/results.mako')
                return template.render(username=u, classtype=c, results=results)
            if (len(results) == 0):
                return template.render(username=u, classtype=c, action="fail")
        else:
            return template.render(username=u, classtype=c, action="noparams")


class IradsSearch(object):

    @cherrypy.expose
    @cherrypy.tools.protect()
    def index(self):
        template = lookup.get_template('search/search.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect()
    def search(self, start=None, end=None, keywords=None, sort=None):
        template = lookup.get_template('search/search_results.mako')
        (u, c) = getUserInfo()
        if not ((start and end and sort) or (keywords and sort)):
            template = lookup.get_template('search/search.mako')
            return template.render(username=u, classtype=c, action="noparams")
        session = database.get()
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
            template = lookup.get_template('search/search.mako')
            return template.render(username=u, classtype=c, action="fail")


class IradsUpload(object):

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['r'])
    def index(self):
        template = lookup.get_template('upload/upload.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['r'])
    def selectRecord(self):
        global database
        template = lookup.get_template('upload/selectrecord.mako')
        (u, c) = getUserInfo()
        session = database.get()
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
        template = lookup.get_template('upload/addrecord.mako')
        (u, c) = getUserInfo()
        session = database.get()
        patients = []
        doctors = []
        for entry in session.query(User).filter(User.class_type == 'p').all():
            if (entry.person.__dict__ not in patients):
                patients.append(entry.person.__dict__)
        for entry in session.query(User).filter(User.class_type == 'd').all():
            if (entry.person.__dict__ not in doctors):
                doctors.append(entry.person.__dict__)
        if (len(patients) == 0):
            template = lookup.get_template('upload/upload.mako')
            return template.render(
                username=u, classtype=c, action="noPatient")
        if (len(doctors) == 0):
            template = lookup.get_template('upload/upload.mako')
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
        template = lookup.get_template('upload/upload.mako')
        (u, c) = getUserInfo()
        if (patient and doctor and test_type and test_date and prescribing_date
                and diagnosis and description):
            session = database.get()
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
        template = lookup.get_template('upload/addimage.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c, id=id)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['r'])
    def postImage(self, id=None, radiologyimage=None):
        template = lookup.get_template('upload/upload.mako')
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
            session = database.get()
            pacsimage = PacsImage(
                record_id=id, thumbnail=thumbstream.getvalue(),
                regular_size=normalstream.getvalue(),
                full_size=fullstream.getvalue())
            session.add(pacsimage)
            session.commit()
            return template.render(username=u, classtype=c, action="added")
        else:
            return template.render(username=u, classtype=c, action="error")


def main():
    global database
    current_dir = os.path.dirname(os.path.abspath(__file__))

    config = {'/': {'tools.staticdir.root': current_dir,
                    'tools.sessions.on': True,
                    'tools.sessions.storage_type': "ram",
                    'tools.sessions.timeout': 3600
                    },
              '/css':
             {'tools.staticdir.on': True, 'tools.staticdir.dir': 'css'},
              '/js':
             {'tools.staticdir.on': True, 'tools.staticdir.dir': 'js'}}

    Mapping = Irads()
    Mapping.analysis = IradsAnalysis()
    Mapping.manager = IradsManager()
    Mapping.report = IradsReport()
    Mapping.search = IradsSearch()
    Mapping.upload = IradsUpload()

    # Connect to the database
    database = Database(connect=True)
    database.connect(
        DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOSTNAME, DATABASE)

    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 27848})
    # Plug it into the quickstart with the default config.
    cherrypy.quickstart(Mapping, '/', config=config)

if (__name__ == '__main__'):
    main()
