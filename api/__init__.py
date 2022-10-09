import logging
from .exceptions import UnauthorizedAccess, ControllerNotFound, DeviceNotFound, \
    CommandNotFound, InvalidRequestBody

logger = logging.getLogger('api')


class HomeAccessApi():

    def __init__(self, flask_app, db):
        self._flask_app = flask_app
        self._db = db

    def authorization(self, vto_user_id, door_id, payload):
        try:
            with self._db:
                with self._db.cursor() as cursor:
                    cursor.execute(
                        "SELECT %s %s", (vto_user_id, door_id))

            logger.info('Controlling %s via %s: %s', device_id, controller_id, payload['command'])
        except Exception as e:
            logger.error("(%s): %s" % (e.__class__.__name__, e))
            return "(%s): %s" % (e.__class__.__name__, e), 400
        else:
            return 'success', 200
