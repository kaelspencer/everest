import networkx as nx
from db import get_all

# This class loads all of the jumps and puts them into a Graph. It then lets the graph
# calculate the jump distance. This class operates soley on system IDs.
class SystemGraph():
    def __init__(self):
        self.g = nx.Graph()
        jumps = get_all('select fromSolarSystemID, toSolarSystemId from eve.mapSolarSystemJumps', {})
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
