import cherrypy
import os.path
from config import *
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
    # Set up CherryPy config
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

    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 27848})

    # Connect to the database
    database = Database(connect=True)
    database.connect(
        DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOSTNAME, DATABASE)

    # Set up CherryPy mapping
    Mapping = Irads(database)
    Mapping.analysis = IradsAnalysis(database)
    Mapping.manager = IradsManager(database)
    Mapping.report = IradsReport(database)
    Mapping.search = IradsSearch(database)
    Mapping.upload = IradsUpload(database)

    # Start
    cherrypy.quickstart(Mapping, '/', config=config)

if (__name__ == '__main__'):
    main()
