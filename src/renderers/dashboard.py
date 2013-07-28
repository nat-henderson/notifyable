from flask import Blueprint
from flask import render_template
from flask.ext.login import login_required
from flask.ext.security.core import current_user
from models import Session, OAuthTokens

dashboard_renderer = Blueprint('dashboard', __name__)

@dashboard_renderer.route('/dashboard/alpha')
@login_required
def render_dashboard():
    if authentication_tokens_present(current_user.id):
        return render_template('dashboard.html')
    else:
        return render_template('fetch_tokens.html')

def authentication_tokens_present(user_id):
    session = Session()
    oauth_tokens = session.query(OAuthTokens).filter_by(user_id=user_id).one()
    return oauth_tokens