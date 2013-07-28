from flask import Blueprint
from models import db, GithubRepo, GithubRepoEvent
import json

gh_renderer = Blueprint('github', __name__)

@gh_renderer.route('/github/<int:repo_id>')
def get_gh_entry(repo_id):
    entry = db.session.query(GithubRepoEvent)\
            .filter_by(repo_id = repo_id)\
            .order_by(GithubRepoEvent.id.desc()).first()
    repo = db.session.query(GithubRepo)\
            .filter_by(id = repo_id).one()
    if not entry:
        return json.dumps({'type' : 'text',
                'color' : '000000',
                'channel' : 'Github',
                'title' : repo.gh_repo,
                'text' : 'No one has committed for a while!'
                'image' : None,
                'meta' : {
                    'text' : 'Github!',
                    'image' : 'http://newmerator.github.io/blacktocat.png'
                },
            })
    return json.dumps({'type' : 'text',
            'color' : '000000',
            'channel' : 'Github',
            'title' : repo.gh_repo,
            'text' : '%s pushed with message %s' % (entry.user_pushed, entry.message),
            'image' : entry.avatar_url,
            'meta' : {
                'text' : 'Github!',
                'image' : 'http://newmerator.github.io/blacktocat.png'
            },
        })
