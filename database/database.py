from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


class Database():
    db = None
    session = None

    def __init__(self, connect=False, shared=True):
        #self.connection = Database.connection
        if not connect:
            self.session = Database.session()

    def connect(self, username, password, host, database):
        # Create a connection and store it in the current thread
        print "Opening SQLAlchemy Connection...",
        Database.db = create_engine('mysql://' + username + ':' +
                                    password + '@' + host + '/' + database, echo=True, encoding='utf8')

        # A factory of sessions
        session_factory = sessionmaker(bind=Database.db)

        # Thread local storage of each session
        Database.session = scoped_session(session_factory)

        print "done."

    def get(self):
        return self.session

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.remove()

    # Commit the transaction and remove the session
    def commitAndClose(self):
        self.commit()
        self.close()

    # Short hand for commitAndClose
    def CAC(self):
        self.commitAndClose()
