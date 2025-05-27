# Solo Project Task 3 - CS163

## Overview

This project is focused on analyzing and visualizing transportation data in Ho Chi Minh City. It involves processing OpenStreetMap (OSM) data, handling vehicle data, and visualizing the results on a map. The project is divided into several modules, each responsible for specific tasks such as graph creation, edge matrix computation, data preprocessing, and visualization.

## Project Structure

### Main Files

- **`main.py`**: The entry point of the project. It integrates various modules to load data, process edges, and validate the program's accuracy.

- **`edge_matrix.py`**: Handles the computation of the intermediate frequency matrix, which identifies the most frequently occurring edges between any two given edges.

- **`functions.py`**: Contains utility functions for parsing data and creating an edge matrix for debugging and testing purposes.

- **`graph.py`**: Creates a graph from the Ho Chi Minh City OSM file, with nodes and edges representing geographical and relational data.

- **`preprocess.py`**: Preprocesses edges in the bus history data to extract corresponding coordinates for visualization.

- **`vehicle.py`**: Defines a `Vehicle` class to encapsulate vehicle data for better querying and manipulation.

- **`visualize.py`**: Visualizes the OSM map and sampled data points using Folium and OSMnx.

### Supporting Files

- **`23125062_Task03.pdf`**: A PDF document, possibly containing the project description or requirements.

- **`README.md`**: This file, providing an overview of the project.

- **`jsonFiles/`**: Contains JSON data files, such as `bus_history.json`, used for processing.

- **`htmlFiles/`**: Includes HTML files for map visualization, such as `hcmc_map.html`.

- **`output/`**: Stores output files like `edge_index.pkl` and `inter_edges_matrix.npz`.

### Figures and Visualizations

- **`figures/`**: Contains images like `figure_1.png` for documentation or analysis.

- **`htmlFiles/`**: Includes interactive map visualizations.

## Key Features

1. **Graph Creation**:
   - Parses OSM data to create a graph with nodes and edges.
   - Handles geographical data with latitude, longitude, and tags.

2. **Edge Matrix Computation**:
   - Computes the frequency of adjacent edges.
   - Saves results in a sparse matrix format for efficient storage.

3. **Data Preprocessing**:
   - Extracts coordinates for edges in the bus history.
   - Prepares data for visualization.

4. **Vehicle Handling**:
   - Encapsulates vehicle data into objects for better querying.
   - Supports operations like retrieving vehicle numbers and routes.

5. **Visualization**:
   - Visualizes the OSM map with sampled nodes and edges.
   - Uses Folium for interactive map rendering.

## Dependencies

- Python libraries:
  - `osmnx`
  - `folium`
  - `tqdm`
  - `scipy`
  - `networkx`
  - `numpy`
  - `json`
  - `pickle`

## How to Run

1. Install the required Python libraries using `pip install -r requirements.txt`.
2. Run `main.py` to execute the project.
3. View the visualizations in the `htmlFiles/` directory.

## Future Work

- Enhance the visualization with more detailed data.
- Optimize the edge matrix computation for larger datasets.
- Add more features for vehicle data analysis.