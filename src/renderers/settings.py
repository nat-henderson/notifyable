from flask import make_response
from flask import Blueprint
from flask import render_template
from flask.ext.login import login_required
from flask.ext.security.core import current_user
from models import Session, OAuthTokens
import tweepy
import json
import random

settings_renderer = Blueprint('settings', __name__)

@settings_renderer.route('/settings', methods=["GET"])
@login_required
def settings():
    oauth_token = get_oauth_token(current_user.id)

    if oauth_token is None:
        return fetch_twitter_tokens(oauth_token)
    if oauth_token.facebook_key is None:
        return fetch_facebook_token(oauth_token)
    else:
        return render_template('settings.html')

def fetch_twitter_tokens(oauth_token):
    config = json.load(open('config.json'))
    consumer_key = str(config["TwitterReader"]["CONSUMER_KEY"])
    consumer_secret = str(config["TwitterReader"]["CONSUMER_SECRET"])
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    twitter_url = auth.get_authorization_url()
    response = make_response(render_template("fetch_token.html", twitter_url=twitter_url))
    response.set_cookie("twitter_key", auth.request_token.key)
    response.set_cookie("twitter_secret", auth.request_token.secret)
    return response

def fetch_facebook_token(oauth_token):
    config = json.load(open('config.json'))
    app_id = str(config["FacebookReader"]["APP_ID"])
    app_secret = str(config["FacebookReader"]["APP_SECRET"])
    scope = str(config["FacebookReader"]["SCOPE"])
    redirect_url = str(config["FacebookReader"]["REDIRECT_URL"])
    facebook_url = "http://www.facebook.com/dialog/oauth/?client_id="+app_id+"&redirect_uri="+redirect_url+"&scope="+scope+"&state="+str(random.randint(1, 1000))
    response = make_response(render_template("fetch_token.html", facebook_url=facebook_url))
    return response
    
def get_oauth_token(user_id):
    session = Session()
    oauth_token = None
    try:
        oauth_token = session.query(OAuthTokens).filter_by(user_id=user_id).one()
    except:
        return None
    return oauth_token
