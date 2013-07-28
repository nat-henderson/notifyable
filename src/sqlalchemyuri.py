import os
basedir = os.path.abspath(os.path.dirname(__file__))
sqlalchemyuri = 'sqlite:///' + os.path.join(basedir, 'app.db')
