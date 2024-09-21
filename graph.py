import osmium
import networkx as nx
import json

"""  
[module: graph]

This module is used to create the graph from HoChiMinh.osm file. 
Each node in the graph is consider carefully with lat, lon and tags.
For way and relation, same structrue is applied. 
"""

# Task 3.1
class OSMHandler(osmium.SimpleHandler):
    def __init__(self):
        super(OSMHandler, self).__init__()
        self.nodes = {}
        self.ways = {}
        self.relations = {}

    def node(self, n):
        self.nodes[n.id] = {
            'lat': n.location.lat,
            'lon': n.location.lon,
            'tags': {t.k: t.v for t in n.tags}
        }

    def way(self, w):
        self.ways[w.id] = {
            'nodes': [n.ref for n in w.nodes],
            'tags': {t.k: t.v for t in w.tags}
        }

    def relation(self, r):
        self.relations[r.id] = {
            'members': [(m.type, m.ref, m.role) for m in r.members],
            'tags': {t.k: t.v for t in r.tags}
        }

def create_graph_from_osm(osm_file):
    handler = OSMHandler()
    handler.apply_file(osm_file)

    G = nx.MultiDiGraph()
    
    total_edges = {}

    # Add nodes
    for node_id, node_data in handler.nodes.items():
        G.add_node(node_id, **node_data)

    # Add edges from ways
    
    """ 
    edges are defined as the line between two intersection
    highway is connected by intersections --> map bus_history
    to intersection for each edge.
    """
    
    for way_id, way_data in handler.ways.items():
        nodes = way_data['nodes']
        tags = way_data['tags']
        if 'highway' in tags:
            G.add_edge(nodes[0], nodes[len(nodes) - 1], wayid=way_id, **tags)
            total_edges[way_id] = nodes
                
    return G, total_edges

def save_total_edges(total_edges):
    with open("output/total_edges", 'w') as f:
        json.dump(total_edges, f)
    print("Save total_edges successfully")

def convert_sub_edges_to_edge(total_edges):
    total_sub_edges = {}
    for edge, nodes in total_edges.items():
        for i in range(len(nodes) - 1):
            total_sub_edges[nodes[i], nodes[i+1]] = edge 
            total_sub_edges[nodes[i+1], nodes[i]] = edge
            
    return total_sub_edges

def save_total_sub_edges(total_sub_edges, filename):
    # Convert tuple keys to string representations and keep values as edge IDs
    total_sub_edges_str_keys = {f'("{k[0]}", "{k[1]}")': v for k, v in total_sub_edges.items()}
    
    with open(filename, 'w') as file:
        json.dump(total_sub_edges_str_keys, file)
    
    print("Save total_sub_edges successfully")
    
# Load graph + Save total edges + Save total sub edges
# G, total_edges = create_graph_from_osm(osm_file="osmFiles/HoChiMinh.osm")
# total_sub_edges = convert_sub_edges_to_edge(total_edges)
# save_total_sub_edges(total_sub_edges, filename="output/total_sub_edges")
# save_total_edges(total_edges)