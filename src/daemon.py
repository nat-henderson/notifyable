import inspect
import api_readers
from api_readers import *
from api_readers.api_reader_daemon import APIReaderDaemon
import json
from multiprocessing import Process

config = json.load(open('config.json'))

class WrapperDaemon(Process):
    def __init__(self, daemon_obj, *args, **kwargs):
        super(WrapperDaemon, self).__init__(*args, **kwargs)
        self.daemon_obj = daemon_obj

    def run(self):
        self.daemon_obj.start()

    def terminate(self):
        self.daemon_obj.stop()
        super(WrapperDaemon, self).terminate()

class MainDaemon(object):
    def __init__(self):
        self.daemons = []
        print 'discovering daemons...'
        for _, daemon_module in inspect.getmembers(api_readers, inspect.ismodule):
            for name, daemon_class in inspect.getmembers(daemon_module, inspect.isclass):
                if (issubclass(daemon_class, APIReaderDaemon)
                        and daemon_class is not APIReaderDaemon):
                    print 'discovered ' + str(name)
                    self.daemons.append(WrapperDaemon(daemon_class(**config.get(name, {}))))

    def setup(self):
        print 'starting daemons ...'
        for daemon in self.daemons:
            print 'started ' + str(daemon.daemon_obj.__class__)
            daemon.start()

    def mainloop(self):
        pass

    def cleanup(self):
        print 'stopping daemons ...'
        for daemon in self.daemons:
            try:
                print 'stopped ' + str(daemon.__class__)
                daemon.terminate()
            except:
                pass

    def start(self):
        try:
            self.setup()
            while True:
                self.mainloop()
        finally:
            self.cleanup()

if __name__ == "__main__":
    MainDaemon().start()
