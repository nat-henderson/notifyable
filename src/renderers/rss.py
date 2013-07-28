from flask import Blueprint
from models import db, RSSEntry
import json

rss_renderer = Blueprint('rss', __name__)

@rss_renderer.route('/rss/<int:feed_id>')
def get_rss_entry(feed_id):
    entry = db.session.query(RSSEntry).order_by(RSSEntry.id.desc()).one()
    return json.dumps({'type' : 'text',
            'color' : '222222',
            'channel' : 'RSS',
            'title' : entry.title,
            'text' : entry.desc,
            'image' : None,
            'meta' : { 'text' : None, 'image' : None },
        })