import cherrypy
import time
from database.mappings import *
from helpers import *
from mako.lookup import TemplateLookup
from sqlalchemy.exc import IntegrityError


class IradsManager(object):

    """Responsible for all management (adding or updating)
    of users, people and family doctors.
    """

    database = None
    lookup = TemplateLookup(directories=['templates'])

    def __init__(self, database):
        self.database = database

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def index(self):
        """Returns the main page of the module which
        allows the administrator to select an action.
        """
        template = self.lookup.get_template('manager/manager.mako')
        (u, c) = getUserInfo()
        return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def addPerson(self, firstname=None, lastname=None,
                  address=None, email=None, phone=None):
        """Returns a page that allows an admin to
        add a person to the system.
        """
        template = self.lookup.get_template('manager/addperson.mako')
        (u, c) = getUserInfo()
        if firstname:
            session = self.database.get()
            person = Person(
                first_name=firstname, last_name=lastname,
                address=address, email=email, phone=phone)
            '''
            INSERT INTO persons (first_name, last_name, address, email, phone)
            VALUES (firstname, lastname, address, email, phone)
            '''
            session.add(person)
            session.commit()
            return template.render(username=u, classtype=c, action=True)
        else:
            return template.render(username=u, classtype=c)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def editPerson(self, id, firstname=None, lastname=None,
                   address=None, email=None, phone=None):
        """Returns a page that allows an admin to
        edit a person's information.
        """
        template = self.lookup.get_template('manager/editperson.mako')
        (u, c) = getUserInfo()
        session = self.database.get()
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
        template = self.lookup.get_template('manager/listperson.mako')
        (u, c) = getUserInfo()
        session = self.database.get()
        persons = []
        for entry in session.query(Person).order_by(Person.last_name).all():
            persons.append(entry.__dict__)
        return template.render(username=u, classtype=c, persons=persons)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def addUser(self, preset, username=None,
                password=None, classtype=None, id=None):
        template = self.lookup.get_template('manager/adduser.mako')
        (u, c) = getUserInfo()
        session = self.database.get()
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
    def editUser(self, userToEdit, password=None, password2=None):
        template = self.lookup.get_template('manager/edituser.mako')
        (u, c) = getUserInfo()
        session = self.database.get()
        user = session.query(User).filter(User.user_name == userToEdit).one()
        fail = False
        if password or password2:
            if password == password2:
                user.password = password
            else:
                fail = True
        if password:
            if not fail:
                session.commit()
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
        template = self.lookup.get_template('manager/listuser.mako')
        (u, c) = getUserInfo()
        session = self.database.get()
        users = []
        for entry in session.query(User).order_by(User.user_name).all():
            users.append(entry.__dict__)
        return template.render(username=u, classtype=c, users=users)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def listDoctor(self):
        template = self.lookup.get_template('manager/listdoctor.mako')
        (u, c) = getUserInfo()
        session = self.database.get()
        doctors = []
        for entry in session.query(
                User).filter(User.class_type == 'd').all():
            if entry.person.__dict__ not in doctors:
                doctors.append(entry.person.__dict__)
        return template.render(username=u, classtype=c, doctors=doctors)