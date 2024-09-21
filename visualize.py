import osmnx as ox
import folium
from folium.plugins import MarkerCluster
import random


"""  
[module: visualization]

This module is used to visualize HCM.osm map for better
handling data and get a good structure
"""

G = ox.graph_from_xml('osmFiles/HoChiMinh.osm')

nodes, edges = ox.graph_to_gdfs(G)

sampled_nodes = nodes.sample(frac=0.1)
sampled_edges = edges.sample(frac=0.1)

m = folium.Map(location=[10.8231, 106.6297], zoom_start=11)

mc = MarkerCluster()
for idx, node in sampled_nodes.iterrows():
    folium.CircleMarker([node['y'], node['x']], radius=2).add_to(mc)
mc.add_to(m)

for idx, edge in sampled_edges.iterrows():
    folium.PolyLine(edge['geometry'].coords, weight=2, color='red').add_to(m)

m.save('hcmc_map.html')