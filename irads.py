import cherrypy
from cgi import escape
from database.mappings import *
from helpers import *
from mako.lookup import TemplateLookup
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


class Irads(object):

    '''
    This class is responsible for the login module and providing
    access to all other modules.
    '''

    database = None
    lookup = TemplateLookup(directories=['templates'])

    def __init__(self, database):
        self.database = database

    # Login page
    @cherrypy.expose
    def index(self, username=None, password=None):
        global database
        template = self.lookup.get_template('login.mako')
        if username and password:
            username = escape(username, True)
            password = escape(password, True)
            session = self.database.get()
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

    # Main home page
    @cherrypy.expose
    @cherrypy.tools.protect()
    def home(self):
        template = self.lookup.get_template('home.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    # Page for editing your own information
    @cherrypy.expose
    @cherrypy.tools.protect()
    def user(self, firstname=None, lastname=None,
             address=None, email=None, phone=None,
             password=None, password2=None):
        template = self.lookup.get_template('user.mako')
        (u, c) = getUserInfo()
        session = self.database.get()
        user = session.query(User).filter(User.user_name == u).one()
        fail = False
        # make sure password was entered correctly
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

    # Logout page, clears session
    @cherrypy.expose
    def logout(self):
        cherrypy.session.delete()
        template = self.lookup.get_template('login.mako')
        return template.render(loginStatus=2)

    # Displays an error message when login failed
    @cherrypy.expose
    def error(self):
        cherrypy.session.delete()
        template = self.lookup.get_template('login.mako')
        return template.render(loginStatus=3)
