from tracemalloc import start
import numpy as np
import heapq
import itertools
from typing import Union

class Graph:
    """
    Class for Minimum Spanning Tree (MST)
    Parameters:
        adjacency_mat : np.ndarray or str
            Adjacency matrix (2D numpy array) or the path to a CSV file containing the array 
    
    Attributes:
        self.adj_mat : np.ndarray
            Adjacency matrix
        self.mst : np.ndarray
            Minimum spanning tree
    """
    def __init__(self, adjacency_mat: Union[np.ndarray, str]):
        """ Unlike project 2, this Graph class takes an adjacency matrix as input. `adjacency_mat` 
        can either be a 2D numpy array of floats or the path to a CSV file containing a 2D numpy array of floats.

        In this project, we will assume `adjacency_mat` corresponds to the adjacency matrix of an undirected graph
        """
        if type(adjacency_mat) == str:
            self.adj_mat = self._load_adjacency_matrix_from_csv(adjacency_mat)
        elif type(adjacency_mat) == np.ndarray:
            self.adj_mat = adjacency_mat
        else: 
            raise TypeError('Input must be a valid path or an adjacency matrix')
        self.mst = None

    def _load_adjacency_matrix_from_csv(self, path: str) -> np.ndarray:
        with open(path) as f:
            return np.loadtxt(f, delimiter=',')

    def construct_mst(self):
        """ Given `self.adj_mat`, the adjacency matrix of a connected undirected graph, implement Prim's 
        algorithm to construct an adjacency matrix encoding the minimum spanning tree of `self.adj_mat`. 
            
        `self.adj_mat` is a 2D numpy array of floats. 
        Note that because we assume our input graph is undirected, `self.adj_mat` is symmetric. 
        Row i and column j represents the edge weight between vertex i and vertex j. An edge weight of zero indicates that no edge exists. 
        
        TODO: 
            This function does not return anything. Instead, store the adjacency matrix 
        representation of the minimum spanning tree of `self.adj_mat` in `self.mst`.
        We highly encourage the use of priority queues in your implementation. See the heapq
        module, particularly the `heapify`, `heappop`, and `heappush` functions.
        """
        # print('Starting MST','\n')
        self.mst = np.zeros(shape=(self.adj_mat.shape[0],self.adj_mat.shape[1]))
        
        # Find connected vertices with an edge greater than 0
        i,j= np.where(self.adj_mat > 0)
        connected_vertices = list(zip(list(i),list(j)))
        # print('connected vertices:', connected_vertices)
        
        # Find connected vertices edge weight
        weight_by_vertex_list = list(zip([self.adj_mat[x] for x in connected_vertices],connected_vertices))
        # print('weight by vertex list:', weight_by_vertex_list)
        
        # Ensure that if there are multiple edges from vertex 0 that (one of) the lowest scoring edge is selected and added to the queue
        starting_vertex_list = list(filter(lambda x: x[1][0] == 0, weight_by_vertex_list)) # filter to vertex 0
        heapq.heapify(starting_vertex_list)

        # Add start vertex to queue and visisted
        queue = []
        heapq.heappush(queue, starting_vertex_list[0])
        visited = [starting_vertex_list[0][1][0]]
        
        # Start MST and continue traversal until all vertices are visited
        # x = 0
        # print('\n')
        while queue:
            # print('MST iteration:', x)
            # print('queue:',queue)
            
            # Pop the lowest weighted edge
            weight, vertices_tuple = heapq.heappop(queue)
            # print('edge weight and vertices:', weight, vertices_tuple)
            # print('visited:', visited)
            # print('current: ', vertices_tuple[1])

            if vertices_tuple[1] not in visited:

                # Add edge weight to MST
                self.mst[vertices_tuple] = weight
                self.mst[vertices_tuple[::-1]] = weight
                
                # Add destination vertex to visited
                visited.append(vertices_tuple[1])

                # Find candidate neighbors that have not been visited and heapify
                vertex_neighbor_list = [x for x in weight_by_vertex_list if x[1][0] == vertices_tuple[1] and x[1][1] not in visited]
                heapq.heapify(vertex_neighbor_list)
                
                # Add candidate neighbors to the queue
                for vertex_neighbor in vertex_neighbor_list:                
                    # print('neighbor: ', vertex_neighbor)
                    heapq.heappush(queue, vertex_neighbor)

                # x+=1
                # print('MST:', '\n', self.mst)
                # print('\n')

        # print('Final MST: ', '\n', self.mst)
        # End MST