'''

This will initialize the tables like so.

users(user_name,password,class,person_id,date_registered)
persons(person_id,first_name,last_name,address,email,phone)
family_doctor(doctor_id,patient_id)
radiology_record(record_id,patient_id,
                 doctor_id,radiologist_id,test_type,
                 prescribing_date,test_date,diagnosis, description)
pacs_images(record_id,image_id,thumbnail,regular_size,full_size)
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, LargeBinary
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


# To store the personal information
class Person(Base):
    __tablename__ = "persons"

    person_id = Column(Integer, primary_key=True)
    first_name = Column(String(24))
    last_name = Column(String(24))
    address = Column(String(128))
    email = Column(String(128), unique=True)
    phone = Column(String(10))


'''
To store the log-in information
Note that a person may have been assigned different user_name(s), depending
on his/her role in the log-in
'''


class User(Base):
    __tablename__ = "users"

    user_name = Column(String(24), primary_key=True)
    password = Column(String(24))
    date_registered = Column(Date)
    person_id = Column(Integer, ForeignKey("persons.person_id"))

    # Check constraint not supported in MySQL
    class_type = Column(String(1), name="class")

    # Relationships
    person = relationship("Person", backref="users")


# To indicate who is whose family doctor
class FamilyDoctor(Base):
    __tablename__ = "family_doctor"

    doctor_id = Column(Integer,
                       ForeignKey('persons.person_id'), primary_key=True)
    patient_id = Column(Integer,
                        ForeignKey('persons.person_id'), primary_key=True)

    # Relationships
    doctor = relationship("Person",
                          foreign_keys=[doctor_id], backref="caresFor")
    patient = relationship("Person",
                           foreign_keys=[patient_id], backref="patient")


# To store the radiology record
class RadiologyRecord(Base):
    __tablename__ = "radiology_record"

    record_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('persons.person_id'))
    doctor_id = Column(Integer, ForeignKey('persons.person_id'))
    radiologist_id = Column(Integer, ForeignKey('persons.person_id'))
    test_type = Column(String(24))
    prescribing_date = Column(Date)
    test_date = Column(Date)
    diagnosis = Column(String(128))
    description = Column(String(1024))

    # Relationships
    doctor = relationship("Person",
                          foreign_keys=[doctor_id],
                          backref="radiologyrecords_doctor")
    patient = relationship("Person",
                           foreign_keys=[patient_id],
                           backref="radiologyrecords")
    radiologist = relationship("Person",
                               foreign_keys=[radiologist_id],
                               backref="radiologyrecords_radiologist")


# To store the pacs images
class PacsImage(Base):
    __tablename__ = "pacs_images"

    record_id = Column(Integer,
                       ForeignKey('radiology_record.record_id'),
                       primary_key=True)
    image_id = Column(Integer, primary_key=True)
    thumbnail = Column(LargeBinary)
    regular_size = Column(LargeBinary)
    full_size = Column(LargeBinary)

    # Relationships
    record = relationship("RadiologyRecord", backref="pacsimage")
