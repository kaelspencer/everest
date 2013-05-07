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
