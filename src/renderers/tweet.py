from flask import Blueprint
from models import Session, Tweet
import json

tweet_renderer = Blueprint('tweet', __name__)

@tweet_renderer.route('/tweets/<int:user_id>')
def get_tweet(user_id):
    # tweet = Session().query(Tweet).filter_by(user_id=user_id).order_by(Tweet.id.desc()).one()
    # return json.dumps({'type' : 'text',
    #         'tweet_text' : tweet.tweet_text,
    #         'tweeted_by' : tweet.tweeted_by,
    #         'image_url' : tweet.pic_url,
    #         'profile_pic': tweet.profile_pic
    #     })
    tweet = get_last_tweet(user_id)
    return json.dumps({'type' : 'text',
            'tweet_text' : tweet.text,
            'tweeted_by' : tweet.author.name,
            'image_url' : tweet.source_url,
            'profile_pic': tweet.user.profile_image_url
        })

def get_last_tweet(user_id):
    oauth_token = Session.query(OAuthToken).filter_by(user_id=user_id).one()
    api = setup_api(oauth_token)
    return api.user_timeline(count = 1)[0]

def setup_api(oauth_token):
    config = json.load(open('config.json'))
    consumer_key = config["TwitterReader"]["CONSUMER_KEY"]
    consumer_secret = config["TwitterReader"]["CONSUMER_SECRET"]
    key = oauth_token.twitter_key
    secret = oauth_token.twitter_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    return tweepy.API(auth)

