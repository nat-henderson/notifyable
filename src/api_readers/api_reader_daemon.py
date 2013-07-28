from models import db

# Base class for all the daemons
class APIReaderDaemon(object):
    session = db.session
    def start(self):
        return
    def stop(self):
        return
