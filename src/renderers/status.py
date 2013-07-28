from flask import Blueprint
from models import db, Status
import json

status_renderer = Blueprint('status', __name__)

@status_renderer.route('/status/<int:user_id>')
def get_status(user_id):
    status = db.session.query(Status).order_by(Status.id.desc()).first()
    return json.dumps({'type' : 'text',
            'color' : '#8A9EBF',
            'channel' : 'Facebook',
            'text' : status.status_text,
            'image' : status.pic_url,
            'meta': {
                'text' : status.posted_by,
                'image': status.profile_pic
            }
        })
