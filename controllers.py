from app import app
from db import get_db
from flask import abort, Response, jsonify
from functools import wraps
from helpers import sys_to_id, sta_to_sysid, staid_to_sysid, sysid_list_to_object
from graph import SystemGraph
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
    usage = {
        'route': 'Use /route/<from>/<to>/ for systems and /route/station/<from>/<to>/ for stations to get route information.',
        'jump': 'Use /jump/<from>/<to>/ for systems and /route/station/<from>/<to>/ for stations to get a jump count.'
    }
    return jsonify(name='everest', github='https://github.com/kaelspencer/everest', author='Kael Spencer', usage=usage)

# This set of methods handles the routes. Ints are needed, but strings can be supplied.
# The route method is appended with two letters that describe the type of parameters.
@app.route('/route/<int:source>/<int:destination>/')
def route_ii(source, destination):
    g = SystemGraph()
    route = g.route(source, destination)
    route = sysid_list_to_object(route)
    count = len(route) - 1
    return jsonify(route=route, count=count)

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

# This set of methods handles the jump counts. Ints are needed, but strings can be supplied.
# The route method is appended with two letters that describe the type of parameters.
@app.route('/jump/<int:source>/<int:destination>/')
def jump_ii(source, destination):
    g = SystemGraph()
    jumps = g.distance(source, destination)
    return jsonify(jumps=jumps)

@app.route('/jump/<source>/<int:destination>/')
@handleLookupError
def jump_si(source, destination):
    i_source = sys_to_id(source)
    return jump_ii(i_source, destination)

@app.route('/jump/<int:source>/<destination>/')
@handleLookupError
def jump_is(source, destination):
    i_destination = sys_to_id(destination)
    return jump_ii(source, i_destination)

@app.route('/jump/<source>/<destination>/')
@handleLookupError
def jump_ss(source, destination):
    i_source = sys_to_id(source)
    i_destination = sys_to_id(destination)
    return jump_ii(i_source, i_destination)

# Same as the above methods, except the source is a station name or ID.
@app.route('/jump/station/<int:source>/<int:destination>/')
@handleLookupError
def jump_station_ii(source, destination):
    sysid_source = staid_to_sysid(source)
    sysid_destination = staid_to_sysid(destination)
    return jump_ii(sysid_source, sysid_destination)

@app.route('/jump/station/<source>/<int:destination>/')
@handleLookupError
def jump_station_si(source, destination):
    sysid_source = sta_to_sysid(source)
    sysid_destination = staid_to_sysid(destination)
    return jump_ii(sysid_source, sysid_destination)

@app.route('/jump/station/<int:source>/<destination>/')
@handleLookupError
def jump_station_is(source, destination):
    sysid_source = staid_to_sysid(source)
    sysid_destination = sta_to_sysid(destination)
    return jump_ii(sysid_source, sysid_destination)

@app.route('/jump/station/<source>/<destination>/')
@handleLookupError
def jump_station_ss(source, destination):
    sysid_source = sta_to_sysid(source)
    sysid_destination = sta_to_sysid(destination)
    return jump_ii(sysid_source, sysid_destination)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
