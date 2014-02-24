from app import app
from db import get_db
from flask import abort, request, Response, jsonify
from werkzeug.contrib.cache import MemcachedCache
from functools import wraps
from helpers import *
from graph import SystemGraph
from industry import Industry
import json
from crossdomain import crossdomain
import traceback

cache = MemcachedCache(['127.0.0.1:11211'])

# This decorator will return a 404 if the queries return no results.
def handleLookupError(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except LookupError:
            print traceback.format_exc()
            abort(404)
    return decorated_function

def cached(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        cache_key = request.path.replace(' ', '_')
        rv = cache.get(cache_key)
        if rv is not None:
            return rv
        rv = f(*args, **kwargs)
        cache.set(cache_key, rv)
        return rv
    return decorated_function

@app.route('/')
@cached
def index():
    usage = {
        'route': 'Use /route/<from>/<to>/ for systems and /route/station/<from>/<to>/ for stations to get route information.',
        'jump': 'Use /jump/<from>/<to>/ for systems and /route/station/<from>/<to>/ for stations to get a jump count.',
        'batch': 'Post to /jump/batch/ json data like this: {\'source\': \'Jita\', \'destinations\': [\'Rens\', \'Ishisomo\']} to get batched jump counts.'
    }
    return jsonify(name='everest', github='https://github.com/kaelspencer/everest', author='Kael Spencer', usage=usage)

@app.route('/jump/batch/', methods=['POST'])
@handleLookupError
def jump():
    if not hasattr(request, 'json'):
        print 'Aborting: request does not have json data.'
        abort(400)
    elif 'source' not in request.json or 'destinations' not in request.json:
        print 'Aborting: request does not have source and\or destination.'
        abort(400)

    g = None
    source = location_lookup(request.json['source'])
    results = []

    for dest in request.json['destinations']:
        try:
            destid = location_lookup(dest)
        except LookupError:
            print 'Did not find ' + dest
            results.append({ 'destination': dest, 'jumps': -1 })
            continue

        cache_key = str(source) + '_' + str(destid)

        cv = cache.get(cache_key)
        if cv is not None:
            results.append({ 'destination': dest, 'jumps': cv })
        else:
            if g is None:
                g = SystemGraph()
            jumps = len(g.route(source, destid)) - 1
            cache.set(cache_key, jumps)
            results.append({ 'destination': dest, 'jumps': jumps })

    return jsonify(source=request.json['source'], destinations=results)

# This set of methods handles the routes. Ints are needed, but strings can be supplied.
# The route method is appended with two letters that describe the type of parameters.
@app.route('/route/<int:source>/<int:destination>/')
@handleLookupError
@cached
def route_ii(source, destination):
    g = SystemGraph()
    route = g.route(source, destination)
    route = sysid_list_to_object(route)
    count = len(route) - 1
    return jsonify(route=route, count=count)

@app.route('/route/<source>/<int:destination>/')
@handleLookupError
@cached
def route_si(source, destination):
    i_source = sys_to_id(source)
    return route_ii(i_source, destination)

@app.route('/route/<int:source>/<destination>/')
@handleLookupError
@cached
def route_is(source, destination):
    i_destination = sys_to_id(destination)
    return route_ii(source, i_destination)

@app.route('/route/<source>/<destination>/')
@handleLookupError
@cached
def route_ss(source, destination):
    i_source = sys_to_id(source)
    i_destination = sys_to_id(destination)
    return route_ii(i_source, i_destination)

# Same as the above methods, except the source is a station name or ID.
@app.route('/route/station/<int:source>/<int:destination>/')
@handleLookupError
@cached
def route_station_ii(source, destination):
    sysid_source = staid_to_sysid(source)
    sysid_destination = staid_to_sysid(destination)
    return route_ii(sysid_source, sysid_destination)

@app.route('/route/station/<source>/<int:destination>/')
@handleLookupError
@cached
def route_station_si(source, destination):
    sysid_source = sta_to_sysid(source)
    sysid_destination = staid_to_sysid(destination)
    return route_ii(sysid_source, sysid_destination)

@app.route('/route/station/<int:source>/<destination>/')
@handleLookupError
@cached
def route_station_is(source, destination):
    sysid_source = staid_to_sysid(source)
    sysid_destination = sta_to_sysid(destination)
    return route_ii(sysid_source, sysid_destination)

@app.route('/route/station/<source>/<destination>/')
@handleLookupError
@cached
def route_station_ss(source, destination):
    sysid_source = sta_to_sysid(source)
    sysid_destination = sta_to_sysid(destination)
    return route_ii(sysid_source, sysid_destination)

# This set of methods handles the jump counts. Ints are needed, but strings can be supplied.
# The route method is appended with two letters that describe the type of parameters.
@app.route('/jump/<int:source>/<int:destination>/')
@handleLookupError
@cached
def jump_ii(source, destination):
    g = SystemGraph()
    jumps = g.distance(source, destination)
    return jsonify(jumps=jumps)

@app.route('/jump/<source>/<int:destination>/')
@handleLookupError
@cached
def jump_si(source, destination):
    i_source = sys_to_id(source)
    return jump_ii(i_source, destination)

@app.route('/jump/<int:source>/<destination>/')
@handleLookupError
@cached
def jump_is(source, destination):
    i_destination = sys_to_id(destination)
    return jump_ii(source, i_destination)

@app.route('/jump/<source>/<destination>/')
@handleLookupError
@cached
def jump_ss(source, destination):
    i_source = sys_to_id(source)
    i_destination = sys_to_id(destination)
    return jump_ii(i_source, i_destination)

# Same as the above methods, except the source is a station name or ID.
@app.route('/jump/station/<int:source>/<int:destination>/')
@handleLookupError
@cached
def jump_station_ii(source, destination):
    sysid_source = staid_to_sysid(source)
    sysid_destination = staid_to_sysid(destination)
    return jump_ii(sysid_source, sysid_destination)

@app.route('/jump/station/<source>/<int:destination>/')
@handleLookupError
@cached
def jump_station_si(source, destination):
    sysid_source = sta_to_sysid(source)
    sysid_destination = staid_to_sysid(destination)
    return jump_ii(sysid_source, sysid_destination)

@app.route('/jump/station/<int:source>/<destination>/')
@handleLookupError
@cached
def jump_station_is(source, destination):
    sysid_source = staid_to_sysid(source)
    sysid_destination = sta_to_sysid(destination)
    return jump_ii(sysid_source, sysid_destination)

@app.route('/jump/station/<source>/<destination>/')
@handleLookupError
@cached
def jump_station_ss(source, destination):
    sysid_source = sta_to_sysid(source)
    sysid_destination = sta_to_sysid(destination)
    return jump_ii(sysid_source, sysid_destination)

def industry(names=False, rigs=True, category=-1, detail=-1):
    if not category in (-1, 6, 7, 8, 18, 22):
        raise LookupError

    i = Industry(names=names, rigs=rigs, category=category, detail=detail)
    items = i.fetch()
    return jsonify(items=items)

@app.route('/industry/all/')
@handleLookupError
def industry_all():
    return industry()

@app.route('/industry/all/names/')
@handleLookupError
def industry_names():
    return industry(names=True)

@app.route('/industry/norigs/')
@handleLookupError
def industry_norigs():
    return industry(rigs=False)

@app.route('/industry/norigs/names/')
@handleLookupError
def industry_norigs_names():
    return industry(names=True, rigs=False)

@app.route('/industry/<int:category>/')
@handleLookupError
def industry_category(category):
    return industry(category=category)

@app.route('/industry/<int:category>/names/')
@handleLookupError
def industry_category_names(category):
    return industry(names=True, category=category)

@app.route('/industry/detail/<int:itemid>/')
@handleLookupError
def industry_detail(itemid):
    return industry(detail=itemid)

@app.route('/industry/detail/<int:itemid>/names/')
@handleLookupError
def industry_detail_names(itemid):
    return industry(names=True, detail=itemid)

@app.after_request
@crossdomain(origin='*', headers=['Origin', 'X-Requested-With', 'Content-Type', 'Accept'])
def after_request(response):
    return response
