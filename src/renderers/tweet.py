from flask import Blueprint
from models import db, Tweet
import json

tweet_renderer = Blueprint('tweet', __name__)

@tweet_renderer.route('/tweets/<int:user_id>')
def get_tweet(user_id):
    tweet = db.session.query(Tweet).order_by(Tweet.id.desc()).one()
    return json.dumps({'type' : 'text',
            'tweet_text' : tweet.tweet_text,
            'tweeted_by' : tweet.tweeted_by,
            'image_url' : tweet.pic_url,
            'profile_pic': tweet.profile_pic
        })
