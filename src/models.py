from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

db = SQLAlchemy()

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class RSSFeed(db.Model):
    __tablename__ = 'rssfeeds'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    feed_url = db.Column(db.String(1024))

class Tweet(db.Model):
    __tablename__ = 'tweet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tweet_text = db.Column(db.String(140))
    pic_url = db.Column(db.String(255))
    tweeted_by = db.Column(db.String(255))
    profile_pic = db.Column(db.String(255))

    def __init__(self, tweet_text, tweeted_by, user_id, profile_pic = None, pic_url = None):
        self.tweet_text = tweet_text;
        self.tweeted_by = tweeted_by;
        self.user_id = user_id
        self.profile_pic = profile_pic;
        self.pic_url = pic_url;

    def add_tweet(self):
        db.session.add(self)
        db.session.commit()


class Endpoint(object):
    def __init__(self, name, endpoint, db_table, relevance_filter = None):
        self.name = name
        self.endpoint = endpoint
        self.db_table = db_table
        self.relevance_filter = relevance_filter

endpoints = [Endpoint('RSS', '/rss/%i', RSSFeed, lambda x: True)]

