from flask import make_response
from flask import Blueprint
from flask import render_template
from flask.ext.login import login_required
from flask.ext.security.core import current_user
from models import Session, OAuthTokens
import tweepy
import json

dashboard_renderer = Blueprint('dashboard', __name__)

@dashboard_renderer.route('/dashboard/alpha')
@login_required
def render_dashboard():
    oauth_token = get_oauth_token(current_user.id)
    if oauth_token:
        return render_template('dashboard.html')
    else:
        return fetch_tokens(oauth_token)

def fetch_tokens(oauth_token):
    config = json.load(open('config.json'))
    consumer_key = str(config["TwitterReader"]["CONSUMER_KEY"])
    consumer_secret = str(config["TwitterReader"]["CONSUMER_SECRET"])
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    twitter_url = auth.get_authorization_url()
    response = make_response(render_template("fetch_token.html", twitter_url=twitter_url))
    response.set_cookie("twitter_key", auth.request_token.key)
    response.set_cookie("twitter_secret", auth.request_token.secret)

    return response

def get_oauth_token(user_id):
    session = Session()
    oauth_token = session.query(OAuthTokens).filter_by(user_id=user_id).one()
    return oauth_token
