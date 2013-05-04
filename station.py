from app import app
from db import get_one

# Convert a system name to a system ID.
def sys_to_id(system):
    row = get_one('select solarSystemID from eve.mapSolarSystems where solarSystemName LIKE %(system)s', { 'system': system })
    return row[0]

# Get the ID of the system that the station resides in.
def sta_to_sysid(station):
    row = get_one('select solarSystemId from eve.staStations where stationName LIKE %(station)s', { 'station': station })
    return row[0]

# Get the ID of the system that the station (ID) resides in.
def staid_to_sysid(station):
    row = get_one('select solarSystemId from eve.staStations where stationID = %(station)s', { 'station': station })
    return row[0]
