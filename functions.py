import json
import numpy as np
import pickle
from collections import defaultdict
from scipy import sparse
from tqdm import tqdm


"""  
[module: adjacent_edge]

This module is used to handle small functions of parsing data 
and create an edge_matrix with weight is the number of frequency
of adjacent edges to test and debug. 

This module is not used for handling task 3.2, 3.3. 
For those tasks, they are on edge_matrix.py.This module 
is used to debug and testing some functions.
"""

json_file = 'jsonFiles/bus_history.json'

def procees_trip(json_file):
    edge_transitions = defaultdict(lambda: defaultdict(int))
    edge_index = {}
    index_count = 0
    
    data = []
    
    with open(json_file, 'r') as f:
        for line in f:
            data.append(json.loads(line.strip()))
        
    for vehicle in data:
        for trip in vehicle['tripList']:
            edges = trip['edgesOfPath2']
            for i in range(len(edges) - 1):
                current_edge = tuple(edges[i])
                next_edge = tuple(edges[i+1])
                
                if current_edge not in edge_index:
                    edge_index[current_edge] = index_count
                    index_count += 1
                
                if next_edge not in edge_index:
                    edge_index[next_edge] = index_count
                    index_count += 1
                    
                edge_transitions[current_edge][next_edge] += 1
        
    return edge_transitions, edge_index

def get_total_edges(json_file):
    total_edges = []
    
    data = []
    with open(json_file, 'r') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    
    for vehicle in data:
        for trip in vehicle['tripList']:
            edges = trip['edgesOfPath2']
            for edge in edges:
                if edge not in total_edges:
                    total_edges.append(edge)
    
    return total_edges

def get_edge_from_index(edge_index):
    total_edges = get_total_edges(json_file)
    index_to_edge = {}
    for edge in total_edges:
        index = edge_index.get(tuple(edge), None)
        index_to_edge[index] = edge
        
    return index_to_edge

def create_edge_matrix(edge_transitions, edge_index):
    matrix_size = len(edge_index)
    row, col, data = [], [], []
    
    for current_edge, transitions in edge_transitions.items():
        i = edge_index[current_edge]
        for next_edge, count in transitions.items():
            j = edge_index[next_edge]
            row.append(i)
            col.append(j)
            data.append(count)
            
    edge_matrix = sparse.csr_matrix((data, (row, col)), shape=(matrix_size, matrix_size))
    return edge_matrix

def save_edge_matrix(edge_matrix, edge_index, matrix_file, index_file):
    sparse.save_npz(matrix_file, edge_matrix)
    with open(index_file, 'wb') as f:
        pickle.dump(edge_index, f)
    
def load_edge_matrix(matrix_file, index_file):
    edge_matrix = sparse.load_npz(matrix_file)
    with open(index_file, 'rb') as f:
        edge_index = pickle.load(f)
    return edge_matrix, edge_index

def process_and_save_matrix():
    edge_transitions, edge_index = procees_trip(json_file)
    edge_matrix = create_edge_matrix(edge_transitions, edge_index)
    save_edge_matrix(edge_matrix, edge_index, matrix_file, index_file)

def find_most_frequent_adj_edge(edge1, edge2, edge_matrix, edge_index):
    rows = get_matrix_rows([edge1, edge2], edge_matrix, edge_index)
    row1_idx = edge_index.get(tuple(edge1), None)
    row2_idx = edge_index.get(tuple(edge2), None)

    if len(rows) == 2:
        
        if row1_idx is not None and row2_idx is not None:
            row1_data = rows.get(row1_idx, {})
            row2_data = rows.get(row2_idx, {})

            most_frequent_edge = None
            max_count = 0

            for col, count in row1_data.items():
                if col in row2_data:
                    total_count = count + row2_data[col]
                    if total_count > max_count:
                        max_count = total_count
                        most_frequent_edge = col

            if most_frequent_edge is not None:
                return most_frequent_edge, max_count, row1_idx, row2_idx

    return None, 0, row1_idx, row2_idx

def print_most_frequent_adj_edge_between_two_edges(edge1, edge2, edge_matrix, edge_index, index_to_edge):
    most_frequent_edge, count, r1idx, r2idx = find_most_frequent_edge(edge1, edge2, edge_matrix, edge_index)
    corresonding_edge = index_to_edge[most_frequent_edge]
    if most_frequent_edge is not None:
        print(f"The most frequent edge between {edge1} (index {r1idx}) and {edge2} (index {r2idx}) is {corresonding_edge} (index {most_frequent_edge})")
        print(f"Total frequencies: {count}")
    else:
        print(f"No edge found between {edge1} (row {r1idx}) and {edge2} (row {r2idx}).")

def get_matrix_rows(edge_list, edge_matrix, edge_index):
    rows = {}
    for edge in edge_list:
        edge = tuple(edge)
        if edge in edge_index:
            idx = edge_index[edge]
            rows[idx] = {}
            current_row = edge_matrix[idx]
            non_zero_cols = current_row.indices
            non_zero_vals = current_row.data
            
            for col, val in zip(non_zero_cols, non_zero_vals):
                rows[idx][col] = val
    
    return rows

def print_rows_from_edge(edge_list, edge_matrix, edge_index):
    result_rows = get_matrix_rows(edge_list, edge_matrix, edge_index)
    print("Retrieved matrix rows:")
    idx = 0
    for row_idx, col_vals in result_rows.items():
        print(f"Edge {edge_list[idx]} - Row {row_idx}:")
        for col_idx, value in col_vals.items():
            print(f"    Column {col_idx} with Value: {value}")
        print()  
        


    







