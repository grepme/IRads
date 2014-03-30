#!/usr/bin/python

import cherrypy
import config
import os.path
from database.database import Database
from database.mappings import *
from helpers import *
from irads import Irads
from iradsanalysis import IradsAnalysis
from iradsmanager import IradsManager
from iradsreport import IradsReport
from iradssearch import IradsSearch
from iradsupload import IradsUpload


def main():
    """Main Irads function.
    Sets everything up and launches our application
    """

    # Set up CherryPy config
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Static directories for serving up various files
    conf = {'/': {'tools.staticdir.root': current_dir,
                  'tools.sessions.on': True,
                  'tools.sessions.storage_type': "ram",
                  'tools.sessions.timeout': 3600
                  },
            '/css':
           {'tools.staticdir.on': True, 'tools.staticdir.dir': 'css'},
            '/doc':
           {'tools.staticdir.on': True, 'tools.staticdir.dir': 'doc'},
            '/js':
           {'tools.staticdir.on': True, 'tools.staticdir.dir': 'js'}}

    # Set up IP address and port
    cherrypy.config.update({'server.socket_host': config.IP,
                            'server.socket_port': config.PORT})

    # Connect to the database
    database = Database(connect=True)
    database.connect(
        config.DATABASE_USERNAME, config.DATABASE_PASSWORD,
        config.DATABASE_HOSTNAME, config.DATABASE)

    # Set up CherryPy mapping
    Mapping = Irads(database)
    Mapping.analysis = IradsAnalysis(database)
    Mapping.manager = IradsManager(database)
    Mapping.report = IradsReport(database)
    Mapping.search = IradsSearch(database)
    Mapping.upload = IradsUpload(database)

    # Start
    cherrypy.quickstart(Mapping, '/', config=conf)

if (__name__ == '__main__'):
    main()
