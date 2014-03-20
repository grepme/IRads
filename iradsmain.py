import cherrypy
import os.path
from authentication import *
from config import *
from mako.lookup import TemplateLookup
from database.database import Database
from database.mappings import *
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

database = None
lookup = TemplateLookup(directories=['templates'])


def getUserInfo():
    return (cherrypy.session.get('username'), cherrypy.session.get('classtype'))


class Irads(object):

    @cherrypy.expose
    def index(self, status=0, username=None, password=None):
        global database
        template = lookup.get_template('login.mako')
        if username and password:
            session = database.get()
            query = session.query(Users).filter(
                Users.user_name == username).filter(Users.password == password)
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
            return template.render(loginStatus=status)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a', 'd', 'p', 'r'])
    def home(self):
        template = lookup.get_template('home.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a', 'd', 'p', 'r'])
    def user(self, password=None):
        template = lookup.get_template('user.mako')
        (u, c) = getUserInfo()
        if password:
            session = database.get()
            user = session.query(Users).filter(Users.user_name == u).one()
            user.password = password
            session.commit()
            return template.render(username=u, classtype=c, action=True)
        else:
            return template.render(username=u, classtype=c)

    @cherrypy.expose
    def logout(self):
        cherrypy.session.delete()
        raise cherrypy.HTTPRedirect('/')


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
    def addPerson(self, firstname=None, lastname=None, address=None, email=None, phone=None):
        template = lookup.get_template('manager/addperson.mako')
        (u, c) = getUserInfo()
        if firstname:
            session = database.get()
            person = Persons(
                first_name=firstname, last_name=lastname,
                address=address, email=email, phone=phone)
            session.add(person)
            session.commit()
            return template.render(username=u, classtype=c, action=True)
        else:
            return template.render(username=u, classtype=c, action=None)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def listPerson(self):
        template = lookup.get_template('manager/listperson.mako')
        (u, c) = getUserInfo()
        session = database.get()
        persons = []
        for entry in session.query(Persons).order_by(Persons.person_id).all():
            persons.append(entry.__dict__)
        return template.render(username=u, classtype=c, persons=persons)


class IradsReport(object):

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def index(self):
        template = lookup.get_template('report/report.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)


class IradsSearch(object):

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a', 'd', 'p', 'r'])
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
        return template.render(username=u, classtype=c, action="none")

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['r'])
    def selectRecord(self):
        global database
        template = lookup.get_template('upload/upload.mako')
        (u, c) = getUserInfo()
        session = database.get()
        user = session.query(Users).filter(Users.user_name == u).one()
        person = session.query(Persons).filter(
            Persons.person_id == user.person_id).one()
        records = person.radiologyrecords_radiologist
        record = []
        for r in records:
            record.append(
                [r.record_id, r.prescribing_date, r.test_date, r.diagnosis, r.description])
        return template.render(username=u, classtype=c, action="selectRecord", records=record)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['r'])
    def addRecord(self):
        template = lookup.get_template('upload/upload.mako')
        (u, c) = getUserInfo()
        p = [["1", "Test"], ["2", "Test"]]
        d = [["1", "Test"], ["2", "Test"]]
        return template.render(username=u, classtype=c, action="addRecord", patients=p, doctors=d)

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
