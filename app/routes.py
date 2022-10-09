from app import app, api
from flask import request


@app.route('/authorization/<vto_user_id>/<door_id>', methods=['POST'])
def post_control(vto_user_id, door_id):
    payload = request.get_json()

    return api.authorization(vto_user_id, door_id, payload)
