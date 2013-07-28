from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask.ext.security.core import current_user
from flask.ext.mail import Mail
from renderers import *
from models import db
from models import *
import os
import json
import inspect
import sys

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'SEEEEEEEKRIT'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECUTIY_CHANGEABLE'] = True
app.config['SECURITY_CONFIRMABLE'] = False
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

# Create database connection object
db.init_app(app)

config = json.load(open('config.json'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

def get_channels_and_endpoints_for_user(user):
    channels = []
    endpoints = []
    for endpoint in endpoints:
        user_rows = db.session.query(endpoint.db_table)\
                .filter_by(user_id = user.get_id())\
                .order_by(endpoint.db_table.id.desc())\
                .limit(5).all()
        if user_rows:
            for row in user_rows:
                channels.append(endpoint.name)
                endpoints.append(endpoint.endpoint % (row.id,))
    return channels, endpoints

# Views
@app.route('/')
@login_required
def home():
    channels, endpoints = get_channels_and_endpoints_for_user(current_user)
    return render_template('index.tmpl', renderers = zip(channels, endpoints))

if __name__ == '__main__':
    db.init_app(app)
    if len(sys.argv) > 1:
        if sys.argv[1] == '--create':
            db.create_all(app=app)
        elif sys.argv[1] == '--drop':
            db.drop_all(app=app)
            db.create_all(app=app)
        else:
            print 'arg not recognized; try --create or --drop'
    else:
        app.run(host='0.0.0.0')
