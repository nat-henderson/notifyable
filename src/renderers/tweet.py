from flask import Blueprint
from models import Session, Tweet
from flask.ext.login import login_required
from flask.ext.security.core import current_user
from models import OAuthTokens
import json
import tweepy
from tweepy.error import TweepError

tweet_renderer = Blueprint('tweets', __name__)

@tweet_renderer.route('/tweets/<int:user_id>')
@login_required
def get_tweet(user_id):
    try:
        tweet = get_last_tweet(current_user.id)
    except TweepError:
        return error_response()

    return json.dumps({'type' : 'text',
            'color' : '#1DADEA',
            'channel' : 'Twitter',
            'title' : tweet.author.name,
            'text' : tweet.text,
            'image' : tweet.user.profile_image_url,
            'meta' : {
                'text' : 'Twitter!',
                'image' : tweet.user.profile_image_url
            },
        })

def get_last_tweet(user_id):
    oauth_token = Session().query(OAuthTokens).filter_by(user_id=user_id).one()
    api = setup_api(oauth_token)
    return api.user_timeline(count = 1)[0]

def setup_api(oauth_token):
    config = json.load(open('config.json'))
    consumer_key = str(config["TwitterReader"]["CONSUMER_KEY"])
    consumer_secret = str(config["TwitterReader"]["CONSUMER_SECRET"])
    key = oauth_token.twitter_key
    secret = oauth_token.twitter_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    return tweepy.API(auth)


def get_image(tweet):
    media = tweet.entities.get('media')
    if media is not None:
        return media[0]['expanded_url']

def error_response():
    return json.dumps({'type' : 'text',
            'color' : '#1DADEA',
            'channel' : 'Twitter',
            'title' : "Authentication Error",
            'text' : 'Unable to connect to Twitter',
            'image' : '',
            'meta' : {
                'text' : 'Twitter!',
                'image' : ''
            },
        })


