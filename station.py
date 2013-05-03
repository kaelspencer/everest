from app import app
from db import get_db

def convert_system_to_id(system):
    db = get_db(app)
    c = db.cursor()
    count = c.execute('select solarSystemID from eve.mapSolarSystems where solarSystemName LIKE %(system)s', { 'system': system })

    if count == 0:
        raise LookupError
    elif count > 1:
        app.logger.warning('Query count %d' % count)

    row = c.fetchone()

    return
