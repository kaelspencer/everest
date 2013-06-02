from app import app
from db import get_one

# Convert a system name to a system ID.
def sys_to_id(system):
    row = get_one('select solarSystemID from mapSolarSystems where solarSystemName LIKE %(system)s', { 'system': system })
    return row[0]

# Get the ID of the system that the station resides in.
def sta_to_sysid(station):
    row = get_one('select solarSystemId from staStations where stationName LIKE %(station)s', { 'station': station })
    return row[0]

# Get the ID of the system that the station (ID) resides in.
def staid_to_sysid(station):
    row = get_one('select solarSystemId from staStations where stationID = %(station)s', { 'station': station })
    return row[0]

# Converts a list of system IDs to system objects.
def sysid_list_to_object(sysids):
    objs = []
    for sys in sysids:
        objs.append(sysid_to_object(sys))
    return objs

# Converts a system ID to a system object.
def sysid_to_object(sysid):
    row = get_one('select solarSystemID, solarSystemName from mapSolarSystems where solarSystemID = %(system)s', { 'system': sysid })
    return { 'id': row[0], 'name': row[1] }

# The source could be either a system or station. Turn it into a system ID.
# A number passed in won't return an error. If it's not a station ID it's assumed to be a system ID.
# A string will throw LookupError if it can't be found as either a system or station.
def location_lookup(source):
    result = source

    if unicode(source).isnumeric():
        # It's a number. It might be a station ID, so try to convert it to a system ID.
        try:
            result = staid_to_sysid(source)
        except LookupError:
            # Not a station ID. Assume it's a system ID and return it.
            pass
    else:
        # First try to convert it as a station to a sys ID.
        # If that fails, try to convert it as a system to a sys ID.
        try:
            result = sta_to_sysid(source)
        except LookupError:
            result = sys_to_id(source)

    return result
