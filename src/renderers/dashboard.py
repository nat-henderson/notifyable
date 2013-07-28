from flask import Blueprint
from flask import render_template
from models import Session, OAuthTokens

dashboard_renderer = Blueprint('dashboard', __name__)

@dashboard_renderer.route('/dashboard/<int:user_id>')
def render_dashboard(user_id):
    if self.authentication_tokens_present(user_id):
        return render_template('dashboard.html')
    else:
        return render_template('fetch_tokens.html')

def authentication_tokens_present(self, user_id):
    session = Session()
    oauth_tokens = session.query(OAuthTokens).filter_by(user_id=user_id).one()
    return oauth_tokens