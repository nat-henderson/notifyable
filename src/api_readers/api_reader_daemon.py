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
    def new_data_received(self, data):
        raise NotImplemented
    def add_to_db(self, data):
        raise NotImplemented
