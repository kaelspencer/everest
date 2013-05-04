from app import app
from db import get_db
from flask import abort, Response, jsonify
from functools import wraps
from station import sys_to_id, sta_to_sysid, staid_to_sysid
import json

# This decorator will return a 404 if the queries return no results.
def handleLookupError(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except LookupError:
            abort(404)
    return decorated_function

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

    return Response(json.dumps(result), mimetype='application/json')

# This set of methods handles the jump counts. Ints are needed, but strings can be supplied.
# The route method is appended with two letters that describe the type of parameters.
@app.route('/route/<int:source>/<int:destination>/')
def route_ii(source, destination):
    return jsonify(source=source, destination=destination)

@app.route('/route/<source>/<int:destination>/')
@handleLookupError
def route_si(source, destination):
    i_source = sys_to_id(source)
    return route_ii(i_source, destination)

@app.route('/route/<int:source>/<destination>/')
@handleLookupError
def route_is(source, destination):
    i_destination = sys_to_id(destination)
    return route_ii(source, i_destination)

@app.route('/route/<source>/<destination>/')
@handleLookupError
def route_ss(source, destination):
    i_source = sys_to_id(source)
    i_destination = sys_to_id(destination)
    return route_ii(i_source, i_destination)

# Same as the above methods, except the source is a station name or ID.
@app.route('/route/station/<int:source>/<int:destination>/')
@handleLookupError
def route_station_ii(source, destination):
    sysid_source = staid_to_sysid(source)
    sysid_destination = staid_to_sysid(destination)
    return route_ii(sysid_source, sysid_destination)

@app.route('/route/station/<source>/<int:destination>/')
@handleLookupError
def route_station_si(source, destination):
    sysid_source = sta_to_sysid(source)
    sysid_destination = staid_to_sysid(destination)
    return route_ii(sysid_source, sysid_destination)

@app.route('/route/station/<int:source>/<destination>/')
@handleLookupError
def route_station_is(source, destination):
    sysid_source = staid_to_sysid(source)
    sysid_destination = sta_to_sysid(destination)
    return route_ii(sysid_source, sysid_destination)

@app.route('/route/station/<source>/<destination>/')
@handleLookupError
def route_station_ss(source, destination):
    sysid_source = sta_to_sysid(source)
    sysid_destination = sta_to_sysid(destination)
    return route_ii(sysid_source, sysid_destination)

@app.route('/jumps/<source>/<destination>/')
def jumps(source, destination):
    app.logger.debug('Traveling from %s to %s' % (source, destination))
    return 'Traveling from {} to {}\n'.format(source, destination)
