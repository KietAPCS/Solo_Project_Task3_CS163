from vehicle import *
from tqdm import tqdm
from folium import PolyLine
import folium
import osmnx as ox
import json
import xml.etree.ElementTree as ET


"""  
[module: preprocessing]

This module is used to preprocess all the edges in the 
bus_history and get the correspondingly coordinates of 
any given edges to draw GeoJSON file.
"""

osm_file_name = "HoChiMinh.osm"

def get_all_node_coordinates(fileName):
    tree = ET.parse(f"osmFiles/{fileName}")
    root = tree.getroot()
    
    node_coordinates = {}
    
    for node in root.findall('node'):
        node_id = node.get('id')
        lat = float(node.get('lat'))
        lon = float(node.get('lon'))
        node_coordinates[node_id] = (lat, lon)
    
    return node_coordinates

busNetwork = VehicleQuery("bus_history.json")
vehicle_history = busNetwork.vehicleList
node_coordinates = get_all_node_coordinates(osm_file_name)

total_edges_nodes = []
for vehicle in vehicle_history:
    for trip in vehicle.getTripList:
        total_edges_nodes.append(trip["edgesOfPath2"])

total_edges_coordinates = []
for trip in total_edges_nodes:
    new_path = []
    for edge in trip:
        lat1, lon1 = node_coordinates[edge[0]]
        lat2, lon2 = node_coordinates[edge[1]]
        new_path.append([[lon1, lat1],[lon2, lat2]])
    total_edges_coordinates.append(new_path)
    






    

