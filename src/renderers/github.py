from flask import Blueprint
from models import db, RSSEntry
import json

gh_renderer = Blueprint('github', __name__)

@gh_renderer.route('/github/<int:repo_id>')
def get_gh_entry(repo_id):
    entry = db.session.query(GithubRepoEvent)\
            .filter_by(GithubRepoEvent.repo_id == repo_id)\
            .order_by(RSSEntry.id.desc()).first()
    repo = db.session.query(GithubRepo)\
            .filter_by(GithubRepo.id == repo_id).one()
    return json.dumps({'type' : 'text',
            'color' : '000000',
            'channel' : 'Github',
            'title' : repo.repo_name,
            'text' : '%s pushed with message %s' % (entry.user_pushed, entry.message),
            'image' : entry.avatar_url,
            'meta' : {
                'text' : 'Github!',
                'image' : 'http://newmerator.github.io/blacktocat.png'
            },
        })
