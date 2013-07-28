from flask import Flask, render_template
from flask import jsonify
from flask.ext.assets import Environment
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask.ext.security.core import current_user
from endpoints import endpoints
from models import db
from models import *
from sqlalchemyuri import sqlalchemyuri
import json
import sys

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'SEEEEEEEKRIT'
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemyuri
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

# Setup Flask to use SCSS
assets = Environment(app)
assets.url = app.static_url_path


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
    return render_template('index.html', renderers = zip(channels, endpoints))

@app.route('/dashboard', methods=["GET"])
@login_required
def dashboard():
    return render_template('dashboard.html')

for endpoint in endpoints:
    app.register_blueprint(endpoint.blueprint)

@app.route('/update/facebook', methods=["GET"])
@login_required
def facebook_test():
    return jsonify(
        type="text",
        color="#FF0000",
        channel="Facebook",
        title="title",
        text="huzzah! This is very long text. Let's see how long I can go just " +
             "babbling on. Yeah, point of this is to stress-test our front-end JS.",
        meta=dict(image="https://si0.twimg"
                    ".com/profile_images/2920991192/957f03ebab5ef48f1363a1378b6a8741_bigger.jpeg", text="Daniel Ge"),
    )

if __name__ == '__main__':
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
