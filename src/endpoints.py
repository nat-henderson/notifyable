from models import RSSFeed, User
from renderers.rss import rss_renderer
from renderers.dashboard import dashboard_renderer
from renderers.github import gh_renderer

class Endpoint(object):
    def __init__(self, name, endpoint, renderer, db_table, relevance_filter = None):
        self.name = name
        self.endpoint = endpoint
        self.blueprint = renderer
        self.db_table = db_table
        self.relevance_filter = relevance_filter

endpoints = [
    Endpoint('RSS', '/rss/%i', rss_renderer, RSSFeed, lambda x: True),
    Endpoint('DashBoard', '/dashboard/%i', dashboard_renderer, User, lambda x: True),
    Endpoint('Github', '/github/%i', gh_renderer, GithubRepo, lambda x:True),
]
