import logging
from datetime import datetime as dt
from psycopg2.extras import RealDictCursor
from .exceptions import *

logger = logging.getLogger('api')


class HomeAccessApi():

    def __init__(self, flask_app, db):
        self._flask_app = flask_app
        self._db = db

    def authorization(self, card_id, door_id):
        try:
            authorized = False
            up = None

            with self._db:
                with self._db.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        "SELECT u.id as uid, u.name, p.name as profile, p.expire_at, "
                        "p.from_hour, p.to_hour, p.from_weekday, p.to_weekday FROM "
                        "\"user\" u INNER JOIN profile p ON (u.profile_id=p.id) WHERE "
                        "u.card_id='%s';" % card_id)
                    up = cursor.fetchone()

                    # User is not found !
                    if up is None:
                        raise UserNotFound(card_id)

                    print('here')
                    logger.debug('Authenticated user (card:%s), checking authorizations ...', card_id)

                    # Expiry check
                    if up['expire_at'] is not None and dt.now().date() > up['expire_at']:
                        raise AccessExpired('%s (uid:%s)' % (up['expire_at'], up['uid']))

                    # Weekday boundaries check
                    if up['from_weekday'] is not None and up['to_weekday'] is not None:
                        weekday = dt.now().toordinal() % 7
                        if weekday < up['from_weekday'] or weekday > up['to_weekday']:
                            raise WeekdayError('current:%s authorization:%s-%s' %
                                               (weekday, up['from_weekday'], up['to_weekday']))

                    # Hour boundaries check
                    if up['from_hour'] is not None and up['to_hour'] is not None:
                        hour = dt.now().hour
                        if hour < up['from_hour'] or hour > up['to_hour']:
                            raise HourError('current:%s authorization:%s-%s' %
                                               (hour, up['from_hour'], up['to_hour']))

                    # Access is granted
                    # @TODO: if notify_on_access then send notification
        except Exception as e:
            logger.error("(%s): %s" % (e.__class__.__name__, e))
            authorized = False
        else:
            logger.info('Authorized user uid:%s card:%s (%s / %s)', up['uid'], card_id, up['name'], up['profile'])
            authorized = True
        finally:
            if up is not None:
                # Log access history if we identified the user
                with self._db:
                    with self._db.cursor(cursor_factory=RealDictCursor) as cursor:
                        cursor.execute(
                            "INSERT INTO history(user_id, created_at, access_granted) VALUES "
                            "(%s, '%s', %s)" % (up['uid'], dt.now(), authorized)
                        )

            if authorized:
                return 'authorized', 200
            else:
                return 'unauthorized', 400
