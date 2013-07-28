from api_readers.api_reader_daemon import APIReaderDaemon
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream

class TwitterReader(APIReaderDaemon):
    consumer_key = "E4TdVoiMVYf44Lvq8KXw"
    consumer_secret = "4xzOk0EvhcDcfBPQ0mJU4PwSeXVNWfOE5sifz4XZ0"

    key = "1626313634-H01bjk5cH4YIYjlI5QF25h799YG3F9rnWpg2ykm"
    secret = "jTtwH8ixH1ImbmAMMyCWTwzYU928m4k40DRFwLe2coQ"

    stream = None

    def start(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.key, self.secret)
        listener = StdOutListener()
        self.stream = Stream(auth, listener)
        self.stream.userstream()

    def stop(self):
        if self.stream is None:
            return
        self.stream.disconnect()



class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

if __name__=="__main__":
    TwitterReader().start()