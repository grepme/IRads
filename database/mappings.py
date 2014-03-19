'''

This will initialize the tables like so.

users(user_name,password,class,person_id,date_registered)
persons(person_id,first_name,last_name,address,email,phone)
family_doctor(doctor_id,patient_id)
radiology_record(record_id,patient_id,doctor_id,radiologist_id,test_type,prescribing_date,test_date,diagnosis, description)
pacs_images(record_id,image_id,thumbnail,regular_size,full_size)
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Date, LargeBinary, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


# To store the personal information
class Persons(Base):
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


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_name = Column(String(24))
    password = Column(String(24))
    data_registered = Column(Date)
    person_id = Column(Integer, ForeignKey("persons.person_id"))

    # Check constraint not supported in MySQL
    class_type = Column(String(1), name="class")

    # Relationships
        person = relationship("Persons", backref="users")


# To indicate who is whose family doctor
class FamilyDoctor(Base):
    __tablename__ = "family_doctor"

    doctor_id = Column(Integer,
                       ForeignKey('persons.person_id'), primary_key=True)
    patient_id = Column(Integer,
                        ForeignKey('persons.person_id'), primary_key=True)

    # Relationships
    doctor = Relationship("Persons",
                          foreign_keys=[doctor_id], backref="caresFor")
    patient = Relationship("Persons",
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
    doctor = Relationship("Persons",
                          foreign_keys=[doctor_id], backref="radiologyrecords_doctor")
    patient = Relationship("Persons",
                           foreign_keys=[patient_id], backref="radiologyrecords")
    radiologist = Relationship("Persons",
                               foreign_keys=[radiologist_id], backref="radiologyrecords_radiologist")


# To store the pacs images
class PacsImages(Base):
    __tablename__ = "pacs_images"

    record_id = Column(Integer,
                       ForeignKey('radiology_record.record_id') primary_key=True)
    image_id = Column(Integer, primary_key=True)
    thumbnail = Column(LargeBinary)
    regular_size = Column(LargeBinary)
    full_size = Column(LargeBinary)

    # Relationships
    doctor = Relationship("RadiologyRecord", backref="pacsimage")
