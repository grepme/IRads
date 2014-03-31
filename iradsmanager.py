import cherrypy
import time
from database.database import Database
from database.mappings import *
from helpers import *
from mako.lookup import TemplateLookup
from sqlalchemy.exc import IntegrityError


class IradsManager(object):

    """Responsible for all management (adding or updating)
    of users, people and family doctors.
    """

    lookup = TemplateLookup(directories=['templates'])

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
            conn = Database()
            session = conn.get()
            person = Person(
                first_name=firstname, last_name=lastname,
                address=address, email=email, phone=phone)
            session.add(person)
            conn.CAC()
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
        conn = Database()
        session = conn.get()
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
            conn.commit()
            person = session.query(Person).filter(Person.person_id == id).one()
            conn.close()
            return template.render(
                username=u, classtype=c, person=person.__dict__, action=True)
        else:
            conn.close()
            return template.render(
                username=u, classtype=c, person=person.__dict__)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def listPerson(self, delete=None, deleteId=None):
        """Returns a page with a list of persons, from which
        one can be selected for editing of their information.

        Also allows for removal of persons.
        """
        template = self.lookup.get_template('manager/listperson.mako')
        (u, c) = getUserInfo()
        conn = Database()
        session = conn.get()
        persons = []
        if delete and deleteId:
            session.query(Person).filter(
                Person.person_id == deleteId).delete()
            session.query(User).filter(
                User.person_id == deleteId).delete()
            conn.commit()
        for entry in session.query(Person).order_by(Person.last_name).all():
            persons.append(entry.__dict__)
        conn.close()
        return template.render(username=u, classtype=c, persons=persons)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def addUser(self, preset, username=None,
                password=None, classtype=None, id=None):
        """Returns a page that allows the addition of a new user.

        If info was passed on, the user is added to the table.
        """
        template = self.lookup.get_template('manager/adduser.mako')
        (u, c) = getUserInfo()
        conn = Database()
        session = conn.get()
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
                conn.CAC()
                return template.render(
                    username=u, classtype=c, persons=persons,
                    preset=int(preset), action="success")
            except IntegrityError:
                conn.close()
                return template.render(
                    username=u, classtype=c, persons=persons,
                    preset=int(preset), action="exists")
        else:
            conn.close()
            return template.render(
                username=u, classtype=c, persons=persons, preset=int(preset))

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def editUser(self, userToEdit, password=None, password2=None):
        """Returns a page that allows the editing of the information
        of a specific user.

        If any information is passed to it,
        it is verified, and if successful, updated.
        """
        template = self.lookup.get_template('manager/edituser.mako')
        (u, c) = getUserInfo()
        conn = Database()
        session = conn.get()
        user = session.query(User).filter(User.user_name == userToEdit).one()
        fail = False
        if password or password2:
            if password == password2:
                user.password = password
            else:
                fail = True
        if password:
            if not fail:
                conn.commit()
            user = session.query(User).filter(
                User.user_name == userToEdit).one()
            conn.close()
            if fail:
                return template.render(username=u, classtype=c,
                                       user=user.__dict__, action="nomatch")
            else:
                return template.render(username=u, classtype=c,
                                       user=user.__dict__, action="success")
        else:
            conn.close()
            return template.render(
                username=u, classtype=c, user=user.__dict__)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def listUser(self, delete=None, deleteId=None):
        """Returns a page with a list of users, from which one can be
        selected for editing.

        Also allows for deletion of users.
        """
        template = self.lookup.get_template('manager/listuser.mako')
        (u, c) = getUserInfo()
        conn = Database()
        session = conn.get()
        users = []
        if delete and deleteId:
            session.query(User).filter(
                User.user_name == deleteId).delete()
            conn.commit()
        for entry in session.query(User).order_by(User.user_name).all():
            users.append(entry.__dict__)
        conn.close()
        return template.render(username=u, classtype=c, users=users)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def listDoctor(self):
        """Returns a page with a list of doctors, from which one can
        be selected for editing of their patients.
        """
        template = self.lookup.get_template('manager/listdoctor.mako')
        (u, c) = getUserInfo()
        conn = Database()
        session = conn.get()
        doctors = []
        for entry in session.query(
                User).filter(User.class_type == 'd').all():
            if entry.person.__dict__ not in doctors:
                doctors.append(entry.person.__dict__)
        conn.close()
        return template.render(username=u, classtype=c, doctors=doctors)

    @cherrypy.expose
    @cherrypy.tools.protect(groups=['a'])
    def editDoctor(self, doctor=None, remove=None, removeId=None, addId=None):
        """Returns a page that lists all the patients currently under
        a family doctor, and allows for adding and removing of patients.
        """
        if doctor is None:
            template = self.lookup.get_template('manager/manager.mako')
            (u, c) = getUserInfo()
            return template.render(username=u, classtype=c, action="noDoctor")
        template = self.lookup.get_template('manager/editdoctor.mako')
        (u, c) = getUserInfo()
        conn = Database()
        session = conn.get()
        if remove and removeId:
            session.query(FamilyDoctor).filter(
                FamilyDoctor.doctor_id == doctor).filter(
                    FamilyDoctor.patient_id == removeId).delete()
        if addId:
            familyDoctor = FamilyDoctor(doctor_id=doctor, patient_id=addId)
            session.add(familyDoctor)
        conn.commit()
        patients = []
        for entry in session.query(
            FamilyDoctor).filter(
                FamilyDoctor.doctor_id == doctor).all():
            if ((entry.patient is not None) and
                    (entry.patient.__dict__ not in patients)):
                patients.append(entry.patient.__dict__)
        people = []
        for entry in session.query(User).filter(User.class_type == 'p').all():
            if ((entry.person.__dict__ not in people) and
                    len(session.query(FamilyDoctor).filter(
                        FamilyDoctor.doctor_id == doctor).filter(
                            FamilyDoctor.patient_id == entry.person.person_id).all()) == 0):
                people.append(entry.person.__dict__)
        conn.close()
        return template.render(
            username=u, classtype=c, doctor=doctor, patients=patients,
            people=people)
