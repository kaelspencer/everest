import networkx as nx
from db import get_all

# This class loads all of the jumps and puts them into a Graph. It then lets the graph
# calculate the jump distance. This class operates soley on system IDs.
class SystemGraph():
    def __init__(self, highonly=False, nohigh=False):
        self.g = nx.Graph()

        if highonly:
            jumps = get_all(g_highonly, {})
        elif nohigh:
            jumps = get_all(g_nohigh, {})
        else:
            jumps = get_all(g_all, {})

        self.g.add_edges_from(jumps)

    # Calculate the number of jumps. Throws LookupError if the nodes weren't found.
    def distance(self, source, destination):
        try:
            return nx.shortest_path_length(self.g, source=source, target=destination)
        except:
            raise LookupError

    # Calculate the route. Throws LookupError if the nodes weren't found.
    def route(self, source, destination):
        try:
            return nx.shortest_path(self.g, source=source, target=destination)
        except:
            raise LookupError

g_highonly = '''
select fromSolarSystemID, toSolarSystemID
from mapSolarSystemJumps t1
    inner join mapSolarSystems t2
        on t1.fromSolarSystemID = t2.solarSystemID
    inner join mapSolarSystems t3
        on t1.toSolarSystemID = t3.solarSystemID
where t2.security >= 0.45 and t3.security >= 0.45;
'''

g_nohigh = '''
select fromSolarSystemID, toSolarSystemID
from mapSolarSystemJumps t1
    inner join mapSolarSystems t2
        on t1.fromSolarSystemID = t2.solarSystemID
    inner join mapSolarSystems t3
        on t1.toSolarSystemID = t3.solarSystemID
where t2.security < 0.45 and t3.security < 0.45;
'''

g_all = '''
select fromSolarSystemID, toSolarSystemId
from mapSolarSystemJumps
'''
