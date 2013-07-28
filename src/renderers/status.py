from flask import Blueprint
from models import db, Status
import json

status_renderer = Blueprint('status', __name__)

@status_renderer.route('/status/<int:user_id>')
def get_status(user_id):
    status = db.session.query(Status).order_by(Status.id.desc()).first()
    return json.dumps({'type' : 'text',
            'status_text' : status.status_text,
            'posted_by' : status.posted_by,
            'image_url' : status.pic_url,
            'profile_pic': status.profile_pic
        })
