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
        'batch': 'Post to /jump/batch/ json data like this: {\'source\': \'Jita\', \'destinations\': [\'Rens\', \'Ishisomo\']} to get batched jump counts.',
        'industry': 'GET /industry/<categoryid>/ to retrieve a list of information on all inventable items in that category. 0 represents all categories. See docs for details.'
    }
    return jsonify(name='everest', github='https://github.com/kaelspencer/everest', author='Kael Spencer', usage=usage, docs='https://github.com/kaelspencer/everest/blob/master/docs/howto.md')

@app.route('/jump/batch/', methods=['POST'])
@handleLookupError
def jump():
    if not hasattr(request, 'json'):
        print 'Aborting: request does not have json data.'
        abort(400)
    elif 'source' not in request.json or 'destinations' not in request.json:
        print 'Aborting: request does not have source and\or destination.'
        abort(400)

    highonly = False
    nohigh = False

    if 'avoidance' in request.json:
        if request.json['avoidance'] == 'high':
            nohigh = True
        elif request.json['avoidance'] == 'highonly':
            highonly = True
        elif request.json['avoidance'] != 'none':
            print 'Aborting: unknown avoidance value: %s' % request.json['avoidance']

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

        avoidance_key = ''
        if highonly:
            avoidance_key = '_highonly'
        elif nohigh:
            avoidance_key = '_nohigh'

        cache_key = str(source) + '_' + str(destid) + avoidance_key

        cv = cache.get(cache_key)
        if cv is not None:
            results.append({ 'destination': dest, 'jumps': cv })
        else:
            if g is None:
                g = SystemGraph(highonly, nohigh)

            try:
                jumps = len(g.route(source, destid)) - 1
                cache.set(cache_key, jumps)
                results.append({ 'destination': dest, 'jumps': jumps })
            except LookupError:
                results.append({ 'destination': dest, 'jumps': -1 })

    return jsonify(source=request.json['source'], destinations=results)

# This set of methods handles the routes. Ints are needed, but strings can be supplied.
# The route method is appended with two letters that describe the type of parameters.
@app.route('/route/<int:source>/<int:destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/route/<int:source>/<int:destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/route/<int:source>/<int:destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def route_ii(source, destination, highonly, nohigh):
    g = SystemGraph(highonly, nohigh)
    route = g.route(source, destination)
    route = sysid_list_to_object(route)
    count = len(route) - 1
    return jsonify(route=route, count=count)

@app.route('/route/<source>/<int:destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/route/<source>/<int:destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/route/<source>/<int:destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def route_si(source, destination, highonly, nohigh):
    i_source = sys_to_id(source)
    return route_ii(i_source, destination, highonly, nohigh)

@app.route('/route/<int:source>/<destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/route/<int:source>/<destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/route/<int:source>/<destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def route_is(source, destination, highonly, nohigh):
    i_destination = sys_to_id(destination)
    return route_ii(source, i_destination, highonly, nohigh)

@app.route('/route/<source>/<destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/route/<source>/<destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/route/<source>/<destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def route_ss(source, destination, highonly, nohigh):
    i_source = sys_to_id(source)
    i_destination = sys_to_id(destination)
    return route_ii(i_source, i_destination, highonly, nohigh)

# Same as the above methods, except the source is a station name or ID.
@app.route('/route/station/<int:source>/<int:destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/route/station/<int:source>/<int:destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/route/station/<int:source>/<int:destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def route_station_ii(source, destination, highonly, nohigh):
    sysid_source = staid_to_sysid(source)
    sysid_destination = staid_to_sysid(destination)
    return route_ii(sysid_source, sysid_destination, highonly, nohigh)

@app.route('/route/station/<source>/<int:destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/route/station/<source>/<int:destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/route/station/<source>/<int:destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def route_station_si(source, destination, highonly, nohigh):
    sysid_source = sta_to_sysid(source)
    sysid_destination = staid_to_sysid(destination)
    return route_ii(sysid_source, sysid_destination, highonly, nohigh)

@app.route('/route/station/<int:source>/<destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/route/station/<int:source>/<destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/route/station/<int:source>/<destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def route_station_is(source, destination, highonly, nohigh):
    sysid_source = staid_to_sysid(source)
    sysid_destination = sta_to_sysid(destination)
    return route_ii(sysid_source, sysid_destination, highonly, nohigh)

@app.route('/route/station/<source>/<destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/route/station/<source>/<destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/route/station/<source>/<destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def route_station_ss(source, destination, highonly, nohigh):
    sysid_source = sta_to_sysid(source)
    sysid_destination = sta_to_sysid(destination)
    return route_ii(sysid_source, sysid_destination, highonly, nohigh)

# This set of methods handles the jump counts. Ints are needed, but strings can be supplied.
# The route method is appended with two letters that describe the type of parameters.
@app.route('/jump/<int:source>/<int:destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/jump/<int:source>/<int:destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/jump/<int:source>/<int:destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def jump_ii(source, destination, highonly, nohigh):
    g = SystemGraph(highonly, nohigh)
    jumps = g.distance(source, destination)
    return jsonify(jumps=jumps)

@app.route('/jump/<source>/<int:destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/jump/<source>/<int:destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/jump/<source>/<int:destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def jump_si(source, destination, highonly, nohigh):
    i_source = sys_to_id(source)
    return jump_ii(i_source, destination, highonly, nohigh)

@app.route('/jump/<int:source>/<destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/jump/<int:source>/<destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/jump/<int:source>/<destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def jump_is(source, destination, highonly, nohigh):
    i_destination = sys_to_id(destination)
    return jump_ii(source, i_destination, highonly, nohigh)

@app.route('/jump/<source>/<destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/jump/<source>/<destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/jump/<source>/<destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def jump_ss(source, destination, highonly, nohigh):
    i_source = sys_to_id(source)
    i_destination = sys_to_id(destination)
    return jump_ii(i_source, i_destination, highonly, nohigh)

# Same as the above methods, except the source is a station name or ID.
@app.route('/jump/station/<int:source>/<int:destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/jump/station/<int:source>/<int:destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/jump/station/<int:source>/<int:destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def jump_station_ii(source, destination, highonly, nohigh):
    sysid_source = staid_to_sysid(source)
    sysid_destination = staid_to_sysid(destination)
    return jump_ii(sysid_source, sysid_destination, highonly, nohigh)

@app.route('/jump/station/<source>/<int:destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/jump/station/<source>/<int:destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/jump/station/<source>/<int:destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def jump_station_si(source, destination, highonly, nohigh):
    sysid_source = sta_to_sysid(source)
    sysid_destination = staid_to_sysid(destination)
    return jump_ii(sysid_source, sysid_destination, highonly, nohigh)

@app.route('/jump/station/<int:source>/<destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/jump/station/<int:source>/<destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/jump/station/<int:source>/<destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def jump_station_is(source, destination, highonly, nohigh):
    sysid_source = staid_to_sysid(source)
    sysid_destination = sta_to_sysid(destination)
    return jump_ii(sysid_source, sysid_destination, highonly, nohigh)

@app.route('/jump/station/<source>/<destination>/', defaults={'highonly': False, 'nohigh': False})
@app.route('/jump/station/<source>/<destination>/highonly/', defaults={'highonly': True, 'nohigh': False})
@app.route('/jump/station/<source>/<destination>/nohigh/', defaults={'highonly': False, 'nohigh': True})
@handleLookupError
@cached
def jump_station_ss(source, destination, highonly, nohigh):
    sysid_source = sta_to_sysid(source)
    sysid_destination = sta_to_sysid(destination)
    return jump_ii(sysid_source, sysid_destination, highonly, nohigh)

def industry(names=False, rigs=True, categories=[0], detail=-1):
    for cat in categories:
        if not cat in (0, 6, 7, 8, 18, 22):
            raise LookupError

    i = Industry(names=names, rigs=rigs, categories=categories, detail=detail)
    items = i.fetch()
    return jsonify(items=items)

@app.route('/industry/<int:category>/', defaults={'names': False, 'rigs': True})
@app.route('/industry/<int:category>/names/', defaults={'names': True, 'rigs': True})
@app.route('/industry/<int:category>/norigs/', defaults={'names': False, 'rigs': False})
@app.route('/industry/<int:category>/names/norigs/', defaults={'names': True, 'rigs': False})
@app.route('/industry/<int:category>/norigs/names/', defaults={'names': True, 'rigs': False})
@handleLookupError
def industry_category(category, names, rigs):
    return industry(categories=[category], names=names, rigs=rigs)

@app.route('/industry/detail/<int:itemid>/', defaults={'names': False})
@app.route('/industry/detail/<int:itemid>/names/', defaults={'names': True})
@handleLookupError
def industry_detail(itemid, names):
    return industry(detail=itemid, names=names)

@app.route('/industry/', methods=['POST'])
@handleLookupError
def industry_post():
    if not hasattr(request, 'json'):
        print 'Aborting: request does not have json data.'
        abort(400)
    elif 'categories' not in request.json:
        print 'Aborting: request does not have categories.'
        abort(400)

    rigs = True
    categories = []
    names = False

    if 'rigs' in request.json:
        rigs = request.json['rigs'] == True

    if 'names' in request.json:
        names = request.json['names'] == True

    for cat in request.json['categories']:
        cat = int(cat)
        if cat not in [0, 6, 7, 8, 18, 22]:
            raise LookupError

        if cat == 0:
            categories = [0]
            break
        else:
            categories.append(cat)

    print 'Categories: %s, Rigs: %s, Names: %s' % (categories, rigs, names)
    return industry(categories=categories, rigs=rigs, names=names)

@app.route('/system/<int:system>/', methods=['GET'])
@app.route('/system/<system>/', methods=['GET'])
@handleLookupError
def system_get(system):
    return system_internal([system])

def system_internal(systems):
    results = []

    for system in systems:
        try:
            sysid = location_lookup(system)
        except LookupError:
            print 'Did not find ' + system
            results.append({ 'solarSystemID': system, 'message': 'Unable to locate this system.' })
            continue

        cache_key = 'system_' + str(sysid)
        cv = cache.get(cache_key)
        if cv is not None and False:
            results.append({ 'destination': dest, 'jumps': cv })
        else:
            try:
                result = get_system_info(sysid)
                results.append(result)
                cache.set(cache_key, result)
            except LookupError:
                results.append({ 'solarSystemID': system, 'message': 'Unable to locate this system.' })

    return jsonify(systems=results)

@app.after_request
@crossdomain(origin='*', headers=['Origin', 'X-Requested-With', 'Content-Type', 'Accept'])
def after_request(response):
    return response
