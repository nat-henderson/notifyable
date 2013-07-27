import inspect
import api_readers
from api_readers import APIReaderDaemon
from api_readers import *

class APIReaderDaemon(object):
    def __init__(self):
        self.daemons = []
        print 'discovering daemons...'
        for name, daemon_class in inspect.getmembers(api_readers, inspect.ismodule):
            if APIReaderDaemon in daemon_class.mro():
                print 'discovered ' + str(name)
                self.daemons.append(APIReaderDaemon(config[name]))

    def setup(self):
        print 'starting daemons ...'
        for daemon in self.daemons:
            print 'started ' + str(daemon.__class__)
            daemon.start()

    def mainloop(self):
        pass

    def cleanup(self):
        print 'stopping daemons ...'
        for daemon in self.daemons:
            print 'stopped ' + str(daemon.__class__)
            daemon.stop()

    def start(self):
        try:
            self.setup()
            while True:
                self.mainloop()
        finally:
            self.cleanup()

if __name__ == "__main__":
    APIReaderDaemon().start()
