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
            try:
                read_feed = feedparser.parse(feed.feed_url)
                if hasattr(read_feed, 'published_parsed'):
                    that_one_time = datetime.datetime.fromtimestamp(time.mktime(read_feed.published_parsed))
                elif hasattr(read_feed, 'updated_parsed'):
                    that_one_time = datetime.datetime.fromtimestamp(time.mktime(read_feed.updated_parsed))
                else:
                    that_one_time = datetime.datetime.now()
                entry = RSSEntry(feed.id, read_feed.entries[0].title,
                        read_feed.entries[0].description,
                        that_one_time)
                self.session.add(entry)
            except:
                continue
        self.session.commit()
        while True:
            sixty_seconds_ago = (datetime.datetime.now() - datetime.timedelta(seconds = 60)).timetuple()
            feeds_to_read = self.session.query(RSSFeed).all()
            for feed in feeds_to_read:
                try:
                    read_feed = feedparser.parse(feed.feed_url)
                    if hasattr(read_feed, 'published_parsed'):
                        that_one_time = datetime.datetime.fromtimestamp(time.mktime(read_feed.published_parsed))
                    elif hasattr(read_feed, 'updated_parsed'):
                        that_one_time = datetime.datetime.fromtimestamp(time.mktime(read_feed.updated_parsed))
                    else:
                        that_one_time = datetime.datetime.now()
                    if read_feed.entries[0].published_parsed > sixty_seconds_ago:
                        entry = RSSEntry(feed.id, read_feed.entries[0].title,
                                read_feed.entries[0].description,
                                that_one_time)
                        self.session.add(entry)
                except:
                    continue
            self.session.commit()
            time.sleep(60)

    def stop(self):
        # we have no resources; we don't care
        pass

if __name__ == '__main__':
    RSSReaderDaemon().start()
