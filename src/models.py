from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemyuri import sqlalchemyuri

db = SQLAlchemy()

def Session():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemyuri
    db = SQLAlchemy(app)
    return db.session

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

class OAuthTokens(db.Model):
    __tablename__ = 'oauthtokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    twitter_key = db.Column(db.String(255), nullable=True)
    twitter_secret = db.Column(db.String(255), nullable=True)
    facebook_key = db.Column(db.String(255), nullable=True)

class RSSFeed(db.Model):
    __tablename__ = 'rssfeeds'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    feed_url = db.Column(db.String(1024))

class RSSEntry(db.Model):
    __tablename__ = 'rssentry'
    id = db.Column(db.Integer, primary_key = True)
    feed_id = db.Column(db.Integer, db.ForeignKey('rssfeeds.id'))
    entry_title = db.Column(db.String(255))
    entry_desc = db.Column(db.String(255))
    entry_pub_time = db.Column(db.DateTime)

class GithubRepo(db.Model):
    __tablename__ = 'github'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    gh_username = db.Column(db.String(255))
    gh_repo = db.Column(db.String(255))

class GithubRepoEvent(db.Model):
    __tablename__ = 'githubevents'
    id = db.Column(db.Integer, primary_key = True)
    repo_id = db.Column(db.Integer, db.ForeignKey('github.id'))

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

class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status_text = db.Column(db.String(140))
    pic_url = db.Column(db.String(255))
    posted_by = db.Column(db.String(255))
    profile_pic = db.Column(db.String(255))

    def __init__(self, status_text, posted_by, user_id, profile_pic = None, pic_url = None):
        self.status_text = status_text;
        self.posted_by = posted_by;
        self.user_id = user_id
        self.profile_pic = profile_pic;
        self.pic_url = pic_url;

    def add_status(self):
        db.session.add(self)
        db.session.commit()



