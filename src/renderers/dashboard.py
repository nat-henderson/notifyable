from flask import Blueprint

dashboard_renderer = Blueprint('dashboard', __name__)

@dashboard_renderer.route('/dashboard/<int:user_id>')
def render_dashboard(user_id):
    return "blarghy blergh"
