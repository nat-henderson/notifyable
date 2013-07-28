from flask import Flask, render_template
from flask import jsonify
from flask import redirect
from flask import url_for
from flask.ext.assets import Environment
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.security import login_required
from flask.ext.security import LoginForm
from flask.ext.security.core import current_user
from endpoints import endpoints
from models import db
from models import *
from models import Session
from sqlalchemyuri import sqlalchemyuri
import json
import sys
from renderers.settings import settings_renderer
from renderers.tweet import tweet_renderer
from flask import request
import tweepy
import urllib2

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
    eps = []
    fb_endpoint = None
    session = Session()
    for endpoint in endpoints:
        print endpoint
        user_rows = session.query(endpoint.db_table)\
                .filter_by(user_id = user.get_id())\
                .order_by(endpoint.db_table.id.desc())\
                .limit(5).all()
        if user_rows:
            for row in user_rows:
                if endpoint.name == "Facebook":
                    fb_endpoint = endpoint.endpoint % row.id
                else:
                    channels.append(endpoint.name)
                    eps.append(endpoint.endpoint % (row.id,))
    channels.append('twitter')
    eps.append('/tweets/1')

    channels.append('Facebook')
    eps.append(fb_endpoint)
    return channels, eps

# Views
@app.route('/')
def home():
    if current_user.is_authenticated():
        return redirect(url_for('dashboard'))
    else:
        form = LoginForm()
        return render_template('index.html', form=form)

@app.route('/dashboard', methods=["GET"])
@login_required
def dashboard():
    channels, endpoints = get_channels_and_endpoints_for_user(current_user)
    return render_template('dashboard.html', renderers=json.dumps(endpoints))

for endpoint in endpoints:
    app.register_blueprint(endpoint.blueprint)
app.register_blueprint(settings_renderer)
app.register_blueprint(tweet_renderer)

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

@app.route('/add_feed_to_db', methods=["GET"])
@login_required
def add_feed_to_db():
    feed_url = request.args["feed_url"]
    feed = RSSFeed(current_user.id, feed_url)
    session = Session()
    session.add(feed)
    session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_github_repo_to_db', methods=["GET"])
@login_required
def add_github_repo_to_db():
    gh_user = request.args["github_user"]
    gh_url = request.args["github_url"]
    repo = GithubRepo(current_user.id, gh_user, gh_url)
    session = Session()
    session.add(repo)
    session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_feed', methods=["GET"])
@login_required
def add_feed():
    return render_template('/add_feed.html')

@app.route('/add_github_repo', methods=["GET"])
@login_required
def add_github_repo():
    return render_template('/add_github_repo.html')

@app.route('/twitter_verification', methods=["GET"])
@login_required
def twitter_verification():
    twitter_key = request.cookies.get('twitter_key')
    twitter_secret = request.cookies.get('twitter_secret')
    config = json.load(open('config.json'))
    consumer_key = str(config["TwitterReader"]["CONSUMER_KEY"])
    consumer_secret = str(config["TwitterReader"]["CONSUMER_SECRET"])
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_request_token(twitter_key, twitter_secret)

    auth.get_access_token(request.args["verification_code"])
    oauthtoken = OAuthTokens()
    oauthtoken.twitter_key = auth.access_token.key
    oauthtoken.twitter_secret = auth.access_token.secret
    oauthtoken.user_id = current_user.id

    session = Session()
    session.add(oauthtoken)
    session.commit()
    return redirect(url_for('dashboard'))

@app.route('/facebook_verification', methods=["GET"])
@login_required
def facebook_verification():
    config = json.load(open('config.json'))
    app_id = str(config["FacebookReader"]["APP_ID"])
    app_secret = str(config["FacebookReader"]["APP_SECRET"])
    verification_code=request.args["code"]
    redirect_url = str(config["FacebookReader"]["REDIRECT_URL"])
    url = "https://graph.facebook.com/oauth/access_token?client_id="+app_id+"&redirect_uri="+redirect_url+"&client_secret="+app_secret+"&code="+verification_code

    req = urllib2.Request(url)
   
    response= urllib2.urlopen(req)
    data=response.read()
    data = data.replace("access_token=","")

    session = Session()
    oauthtoken = session.query(OAuthTokens).filter_by(user_id=current_user.id).one()
    oauthtoken.facebook_key = data
    
    session.commit()
    return redirect(url_for('dashboard'))

@app.route('/update/dropbox', methods=["GET"])
@login_required
def dropbox_test():
    return jsonify(
        type="image",
        color="#0000AA",
        channel="Instagram",
        title="Sutro Tower",
        text="View from the Sunset district in SF",
        image="https://photos-6.dropbox.com/t/0/AAAEmjbQ2wjPZzAd2u2AwEMCBk4PqR1nvSxdW-XGDUt0pw/12/2869254/jpeg/1024x768/3/1374991200/0/2/2013-07-12%2012.57.23.jpg/wutcx6QeYVbYTts7cHuwmGyNpGz8ve4YSHaN4gZbOqQ",
        meta=dict(image="https://si0.twimg"
                        ".com/profile_images/2920991192/957f03ebab5ef48f1363a1378b6a8741_bigger.jpeg",
                        text="I Am Not Joshua Schwarz"),
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
