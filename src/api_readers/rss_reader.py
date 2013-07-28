from api_reader_daemon import APIReaderDaemon
from models import RSSFeed, RSSEntry
import time
import datetime
import feedparser

class RSSReaderDaemon(APIReaderDaemon):
    def __init__(self, **kwargs):
        # we're just accessing content over the public web
        # we don't need anything special.
        pass

    def start(self):
        feeds_to_read = self.session.query(RSSFeed).all()
        for feed in feeds_to_read:
            read_feed = feedparser.parse(feed.feed_url)
            entry = RSSEntry(feed.feed_id, read_feed.entries[0].title,
                    read_feed.entries[0].description, read_feed.published_parsed)
            self.session.add(entry)
        self.session.commit()
        while True:
            for feed in feeds_to_read:
                read_feed = feedparser.parse(feed.feed_url)
                sixty_seconds_ago = (datetime.datetime.now() - datetime.timedelta(seconds = 60)).timetuple()
                if read_feed.entries[0].published_parsed > sixty_seconds_ago:
                    entry = RSSEntry(feed.feed_id, read_feed.entries[0].title,
                            read_feed.entries[0].description, read_feed.published_parsed)
                    self.session.add(entry)
            self.session.commit()
            time.sleep(60)

    def stop(self):
        # we have no resources; we don't care
        pass
