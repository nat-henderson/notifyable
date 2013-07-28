from api_reader_daemon import APIReaderDaemon
import tweepy
from tweepy.streaming import StreamListener
from tweepy.utils import import_simplejson
from tweepy import Stream
from models import Tweet

json = import_simplejson()


class TwitterReader(APIReaderDaemon):
    consumer_key = "E4TdVoiMVYf44Lvq8KXw"
    consumer_secret = "4xzOk0EvhcDcfBPQ0mJU4PwSeXVNWfOE5sifz4XZ0"

    key = "1626313634-H01bjk5cH4YIYjlI5QF25h799YG3F9rnWpg2ykm"
    secret = "jTtwH8ixH1ImbmAMMyCWTwzYU928m4k40DRFwLe2coQ"
    user_id = 15

    stream = None

    def __init__(self, **kwargs):
        if kwargs is None:
            return
        self.consumer_key = kwargs['CONSUMER_KEY']
        self.consumer_secret = kwargs['CONSUMER_SECRET']
        self.key = kwargs['KEY']
        self.secret = kwargs['SECRET']
        self.user_id = kwargs['USER_ID']


    def start(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.key, self.secret)
        listener = TweetListener()
        self.stream = Stream(auth, listener)
        self.stream.userstream()


    def stop(self):
        if self.stream is None:
            return
        self.stream.disconnect()


class TweetListener(StreamListener):
    def on_data(self, data):
        json_data = json.loads(data)
        tweet = Tweet(json_data['text'], json_data['user']['name'], self.user_id)
        tweet.add_tweet()

    def on_error(self, status):
        print status


if __name__ == "__main__":
    TwitterReader().start()