from api_readers.api_reader_daemon import APIReaderDaemon
import tweepy

class TwitterReader(APIReaderDaemon):
    consumer_key = "E4TdVoiMVYf44Lvq8KXw"
    consumer_secret = "4xzOk0EvhcDcfBPQ0mJU4PwSeXVNWfOE5sifz4XZ0"

    key = "1626313634-H01bjk5cH4YIYjlI5QF25h799YG3F9rnWpg2ykm"
    secret = "jTtwH8ixH1ImbmAMMyCWTwzYU928m4k40DRFwLe2coQ"

    def start(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(key, secret)

