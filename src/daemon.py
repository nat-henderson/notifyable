import inspect
import api_readers
from api_readers import *
from api_readers.api_reader_daemon import APIReaderDaemon
import json

config = json.load(open('config.json'))

class MainDaemon(object):
    def __init__(self):
        self.daemons = []
        print 'discovering daemons...'
        for _, daemon_module in inspect.getmembers(api_readers, inspect.ismodule):
            for name, daemon_class in inspect.getmembers(daemon_module, inspect.isclass):
                if issubclass(daemon_class, APIReaderDaemon):
                    print 'discovered ' + str(name)
                    self.daemons.append(daemon_class(config[name]))

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
    MainDaemon().start()
