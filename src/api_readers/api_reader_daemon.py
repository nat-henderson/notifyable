from models import db

# Base class for all the daemons
class APIReaderDaemon(object):
    session = db.session
    def __init__(self, **kwargs):
        raise NotImplemented
    def start(self):
        raise NotImplemented
    def stop(self):
        raise NotImplemented
