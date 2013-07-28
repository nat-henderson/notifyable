from models import RSSFeed, GithubRepo, Status, Tweet
from renderers.rss import rss_renderer
from renderers.github import gh_renderer
from renderers.status import status_renderer
from renderers.tweet import tweet_renderer


class Endpoint(object):
    def __init__(self, name, endpoint, renderer, db_table, relevance_filter = None):
        self.name = name
        self.endpoint = endpoint
        self.blueprint = renderer
        self.db_table = db_table
        self.relevance_filter = relevance_filter

endpoints = [
    Endpoint('RSS', '/rss/%i', rss_renderer, RSSFeed, lambda x: True),
    Endpoint('Github', '/github/%i', gh_renderer, GithubRepo, lambda x:True),
    Endpoint('Facebook', '/facebook', status_renderer, Status, lambda x:True),
    Endpoint('Twitter', '/tweets', tweet_renderer, Tweet, lambda x:True),
]
