import networkx as nx
from db import get_all

# This class loads all of the jumps and puts them into a Graph. It then lets the graph
# calculate the jump distance.
class SystemGraph():
    def __init__(self):
        self.g = nx.Graph()
        jumps = get_all('select fromSolarSystemID, toSolarSystemId from mapSolarSystemJumps', {})
        self.g.add_edges_from(jumps)

    # Calculate the number of jumps. A return value of -1 indicates an error.
    def distance(self, source, destination):
        try:
            jumps = nx.shortest_path_length(self.g, source=source, target=destination)
        except:
            jumps = -1
        return jumps
