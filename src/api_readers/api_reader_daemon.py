from models import Session

# Base class for all the daemons
class APIReaderDaemon(object):
    session = Session()
    def start(self):
        raise NotImplementedError()
    def stop(self):
        raise NotImplementedError()
    def new_data_received(self, data):
        raise NotImplementedError()
    def add_to_db(self, data):
        raise NotImplementedError()
