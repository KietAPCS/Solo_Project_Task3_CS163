import json
import pickle
import time
from graph import *
from scipy import sparse
from scipy.sparse import csr_matrix
from multiprocessing import Pool, cpu_count
from collections import defaultdict
from tqdm import tqdm


"""  
[module: intermediate_frequency_matrix]

This module is used to handle the key problem which is
finding the most ocurring edge between any two given
edges in the matrix and save it to file.
"""

# Task 3.2 + 3.3
json_file = 'jsonFiles/bus_history.json'
matrix_file = 'output/inter_edges_matrix.npz'
index_file = 'output/edge_index.pkl'
osm_file = "osmFiles/HoChiMinh.osm"
total_sub_edges_file = "output/total_sub_edges"

def default_factory():
    return defaultdict(int)

def process_intermediate_edges(trip, total_sub_edges):
    edge_freq = defaultdict(default_factory)
    sub_edges = trip['edgesOfPath2']

    # Map to edge: connection between two intersections
    edges = []
    for sub_edge in sub_edges:
        if tuple(sub_edge) not in total_sub_edges:
            continue
        edge = total_sub_edges[tuple(sub_edge)]
        if edge not in edges:
            edges.append(edge)
    n = len(edges)

    # O(N^3): Max accuracy (Naive Approach)
    # for i in range(n - 2):
    #     edge_i = edges[i]
    #     for j in range(i + 2, n):
    #         edge_j = edges[j]
    #         for k in range(i + 1, j):
    #             intermediate_edge = edges[k]
    #             edge_freq[(edge_i, edge_j)][intermediate_edge] += 1
    
    # O(N * Windows^2) (Sliding Windows)
    # windows = 10
    # for i in range(n):
    #     edge_i = edges[i]
    #     for j in range(i + 2, min(n, i + windows)):
    #         edge_j = edges[j]
    #         for k in range(i + 2, j):
    #             intermediate_edge = edges[k]
    #             edge_freq[(edge_i, edge_j)][intermediate_edge] += 1
                
    # O(N * Windows) (Average case), O(N * Windows^2) (Worst case) (Sliding Windows + Prefix Sum)
    windows = 10 # Can be enlarged (based on computer's cpu performance)
    for i in range(n):
        edge_i = edges[i]
        inter_counts = defaultdict(int)
        for j in range(i + 1, min(n, i + windows + 1)):
            edge_j = edges[j]
            
            if j > i + 1:
                for middle_edge, count in inter_counts.items():
                    edge_freq[(edge_i, edge_j)][middle_edge] += count
                
            inter_counts[edge_j] += 1
        
    return {k: dict(v) for k, v in edge_freq.items()}

def merge_edges_frequency(edge_freqs_list):
    merged_freq = defaultdict(lambda: defaultdict(int))
    for edge_freq in edge_freqs_list:
        for (edge_i, edge_j), inter_edges in edge_freq.items():
            for intermediate_edge, count in inter_edges.items():
                merged_freq[(edge_i, edge_j)][intermediate_edge] += count
                #print(f"From {edge_i} to {edge_j} : {intermediate_edge, count}")
    return merged_freq

def parse_raw_data(json_file, total_sub_edges):
    data = []

    try:
        with open(json_file, 'r') as f:
            for line in f:
                data.append(json.loads(line.strip()))

        print(f"Loaded {len(data)} vehicles from {json_file}")
        
        # Process the trips in parallel
        with Pool(cpu_count()) as pool:
            try:
              
                trip_edges_freq = pool.starmap(process_intermediate_edges, 
                                               [(trip, total_sub_edges) for vehicle in tqdm(data) for trip in vehicle['tripList']])

                print(f"Processed {len(trip_edges_freq)} trips")

                return trip_edges_freq

            except Exception as e:
                print(f"Error during parallel processing: {e}")
                raise

    except FileNotFoundError:
        print(f"File {json_file} not found.")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
    
def get_edge_index(total_edges):
    edge_index = {}
    index_count = 1
    
    for edge, nodes in total_edges.items():
        edge_index[edge] = index_count
        index_count += 1
                        
    return edge_index

def from_index_to_edge(total_edges, index):
    edge_index = load_edge_index(index_file)
    for edge in total_edges:
        if edge_index[edge] == index:
            return edge
    return None
    
def create_inter_edges_matrix(edge_freq, edge_size, edge_index):
    row_indices = []
    col_indices = []
    data = []
    
    for (edge_i, edge_j), inter_edges in edge_freq.items():
        most_frequent_edge = max(inter_edges, key=inter_edges.get)
        row_indices.append(edge_index[str(edge_i)])
        col_indices.append(edge_index[str(edge_j)])
        data.append(edge_index[str(most_frequent_edge)]) 
        
        # if (edge_index[edge_i] == 1):
        #     print(f"From {edge_i, edge_index[edge_i]} to {edge_j, edge_index[edge_j]} : {most_frequent_edge, edge_index[most_frequent_edge]}, ")
            
    inter_edges_matrix = sparse.csr_matrix((data, (row_indices, col_indices)), shape=(edge_size+1, edge_size+1))

    return inter_edges_matrix

def save_inter_edges_matrix(inter_edges_freq, matrix_size, edge_index):
    sparse_matrix = create_inter_edges_matrix(inter_edges_freq, matrix_size, edge_index)
    sparse.save_npz(matrix_file, sparse_matrix) 
    print("Save edge_matrix successfully")
    
def load_inter_edges_matrix(matrix_file):
    sparse_matrix = sparse.load_npz(matrix_file)
    print("Load edge_matrix successfully")
    return sparse_matrix

def save_edge_index(index_file, edge_index):
    with open(index_file, 'wb') as f:
        pickle.dump(edge_index, f)
    print("Save edge_index successfully")

def load_edge_index(index_file):
    with open(index_file, 'rb') as f:
        edge_index = pickle.load(f)
    print("Load edge_index successfully")
    return edge_index

def load_total_sub_edges(filename):
    total_sub_edges = {}
    
    with open(filename, 'r') as file:
        data = json.load(file)
    for key, value in data.items():
        node1, node2 = key.strip('()').split(', ')
        node1 = node1.strip('"')
        node2 = node2.strip('"')
        total_sub_edges[(node1, node2)] = value
        
    print("Load total_sub_edges successfully")
    
    return total_sub_edges

def load_total_edges():
    with open("output/total_edges", "r") as file:
        total_edges = json.load(file)
        
    print("Load total_edges successfully")
        
    return total_edges

def get_rows_from_matrix(edge_list, edge_matrix, edge_index):
    rows = defaultdict(dict)
    for edge in edge_list:
        if edge in edge_index:
            idx = edge_index[edge]
            current_row = edge_matrix[idx]
            for col, val in zip(current_row.indices, current_row.data):
                rows[idx][col] = val
    return dict(rows)

# if __name__ == '__main__':
    # Load total edges
    # total_sub_edges = load_total_sub_edges(total_sub_edges_file)
    # total_edges = load_total_edges()
    
    # Save edge_index
    # edge_index = get_edge_index(total_edges)
    # save_edge_index(index_file, edge_index)
    
    # Load raw data and save to matrix (sparse)
    # edge_index = load_edge_index(index_file)
    # matrix_size = len(edge_index)
    # time1 = time.time()
    # raw_data = parse_raw_data(json_file, total_sub_edges)
    # inter_edges_freq = merge_edges_frequency(raw_data)
    # time2 = time.time()
    # print(f"Processing time: {time2-time1}s")
    # save_inter_edges_matrix(inter_edges_freq, matrix_size, edge_index)
    
# Result of saving matrix
# Load total_sub_edges successfully
# Load total_edges successfully
# Load edge_index successfully
# Loaded 3347 vehicles from jsonFiles/bus_history.json
# 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 3347/3347 [00:00<00:00, 412698.01it/s]
# Processed 13944 trips
# Processing time: 61.42560863494873s
# Save edge_matrix successfully