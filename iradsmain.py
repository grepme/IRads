import cherrypy
import os.path
import time
from config import *
from helpers import *
from mako.lookup import TemplateLookup
from database.database import Database
from database.mappings import *
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

database = None
lookup = TemplateLookup(directories=['templates'])


class Irads(object):

    @cherrypy.expose
    def index(self, username=None, password=None):
        global database
        template = lookup.get_template('login.mako')
        if username and password:
            session = database.get()
            query = session.query(User).filter(
                User.user_name == username).filter(User.password == password)
            try:
                cherrypy.session['username'] = query.one().user_name
                cherrypy.session['classtype'] = query.one().class_type
                raise cherrypy.HTTPRedirect("/home")
            except NoResultFound:
                template = lookup.get_template('login.mako')
                return template.render(loginStatus=1)
            except MultipleResultsFound:
                template = lookup.get_template('login.mako')
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
            date = time.strftime("%Y-%m-%d")
            user = User(user_name=username, password=password,
                        class_type=classtype, person_id=id,
                        date_registered=date)
            session.add(user)
            session.commit()
            return template.render(
                username=u, classtype=c, persons=persons,
                preset=int(preset), action=True)
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


class IradsReport(object):

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def index(self):
        template = lookup.get_template('report/report.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)


class IradsSearch(object):

    @cherrypy.expose
    @cherrypy.tools.protect()
    def index(self):
        template = lookup.get_template('search/search.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)


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
        template = lookup.get_template('upload/upload.mako')
        (u, c) = getUserInfo()
        session = database.get()
        user = session.query(User).filter(User.user_name == u).one()
        person = session.query(Person).filter(
            Person.person_id == user.person_id).one()
        records = person.radiologyrecords_radiologist
        record = []
        for r in records:
            record.append(
                [r.record_id, r.prescribing_date, r.test_date, r.diagnosis,
                 r.description])
        return template.render(
            username=u, classtype=c, action="selectRecord", records=record)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['r'])
    def addRecord(self):
        template = lookup.get_template('upload/upload.mako')
        (u, c) = getUserInfo()
        p = [["1", "Test"], ["2", "Test"]]
        d = [["1", "Test"], ["2", "Test"]]
        return template.render(
            username=u, classtype=c, action="addRecord", patients=p, doctors=d)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['r'])
    def upload(self, id):
        template = lookup.get_template('upload/upload.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c, action="selectImage")


def main():
    global database
    current_dir = os.path.dirname(os.path.abspath(__file__))

    config = {'/': {'tools.staticdir.root': current_dir,
                    'tools.sessions.on': True,
                    'tools.sessions.storage_type': "ram",
                    'tools.sessions.timeout': 3600
                    },
              '/css':
             {'tools.staticdir.on': True, 'tools.staticdir.dir': 'css'}}

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
