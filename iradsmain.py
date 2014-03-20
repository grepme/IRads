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
    def index(self, status=0):
        template = lookup.get_template('login.mako')
        return template.render(loginStatus=status)

    @cherrypy.expose
    def checkLogin(self, username=None, password=None):
        global database
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

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a', 'd', 'p', 'r'])
    def home(self):
        template = lookup.get_template('home.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    @cherrypy.expose
    def logout(self):
        cherrypy.session.delete()
        return self.index(2)


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
        return template.render(username=u, classtype=c)


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
