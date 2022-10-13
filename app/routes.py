from app import app, api


@app.route('/authorization/<card_id>/<door_id>', methods=['POST'])
def post_control(card_id, door_id):
    return api.authorization(card_id, door_id)
