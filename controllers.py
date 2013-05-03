from app import app
from db import get_db
from flask import abort
from station import convert_system_to_id
import json

@app.route('/')
def index():
    db = get_db(app)
    c = db.cursor()
    c.execute('select solarSystemName from eve.mapSolarSystems limit 10')

    columns = [desc[0] for desc in c.description]
    result = []
    rows = c.fetchall()

    for row in rows:
        row = dict(zip(columns, row))
        result.append(row)

    return json.dumps(result, indent=4) + '\n'

# This set of methods handles the jump counts. Ints are needed, but strings can be supplied.
# The route method is appended with two letters that describe the type of parameters.
@app.route('/route/<int:source>/<int:destination>/')
def route_ii(source, destination):
    return 'route_ii\n'

@app.route('/route/<source>/<int:destination>/')
def route_si(source, destination):
    try:
        convert_system_to_id(source)
    except LookupError:
        abort(404)

    return 'route_si\n'

@app.route('/route/<int:source>/<destination>/')
def route_is(source, destination):
    return 'route_is\n'

@app.route('/route/<source>/<destination>/')
def route_ss(source, destination):
    return 'route_ss\n'

@app.route('/jumps/<source>/<destination>/')
def jumps(source, destination):
    app.logger.debug('Traveling from %s to %s' % (source, destination))
    return 'Traveling from {} to {}\n'.format(source, destination)
