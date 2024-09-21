import json
import numpy as np
import pickle
from collections import defaultdict
from scipy import sparse
from tqdm import tqdm
from graph import *
from edge_matrix import *
    
# Must-have
edge_index = load_edge_index(index_file)
matrix_size = len(edge_index)
total_sub_edges = load_total_sub_edges(total_sub_edges_file)

inter_edges_matrix = load_inter_edges_matrix(matrix_file)

edgeHistory = [["3342113667","6768412184"], ["5738080746","3220146382"], ["3915814322","5777195880"], ["5740180436","5755254579"],
               ["2240993963","9432516568"]]
edgeList = []

# Check for accuracy of the program, take some edge on the bus_history, map with its edge in HoChiMinh.osm, then check for
# the corresponding row in the sparse matrix (edge matrix)

print()

for edge in edgeHistory:
    corresponding_edge = total_sub_edges[tuple(edge)]
    print(f"History sub_edge: {edge} -> edge (HoChiMinh.osm) : {corresponding_edge} -> index : {edge_index[str(corresponding_edge)]}")
    edgeList.append(str(corresponding_edge))

res = get_rows_from_matrix(edgeList, inter_edges_matrix, edge_index)

print()

for data, inters in res.items():
    print(f"Row {data}:")
    print(inters)
    print()
