import numpy as np
import heapq
import itertools
from typing import Union

class Graph:
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
    
    def _create_vertex_list(self, i,j):
        return list(zip(list(i),list(j)))

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
        self.mst = np.zeros(shape=(self.adj_mat.shape[0],self.adj_mat.shape[1]))
        i,j= np.where(self.adj_mat > 0)
        connected_vertices = self._create_vertex_list(i,j)
        weight_by_vertex_list = list(zip([self.adj_mat[x] for x in connected_vertices],connected_vertices))
        heapq.heapify(weight_by_vertex_list)
        print('weight by vertex list', weight_by_vertex_list)
        queue = []
        heapq.heappush(queue,weight_by_vertex_list[0])
        visited = [weight_by_vertex_list[0][1][0]]
        x =0
        while queue:
            print('MST iteration: ', x)
            print('queue:',queue)
            weight, vertices_tuple = heapq.heappop(queue)
            print('edge weight and vertices:', weight, vertices_tuple)
            print('visited:', visited)
            if vertices_tuple[1] not in visited:
                self.mst[vertices_tuple] = weight
                self.mst[vertices_tuple[::-1]] = weight
                visited.append(vertices_tuple[1])
                neighbors_list = [x for x in weight_by_vertex_list if x[1][0] == vertices_tuple[1]] # and x[1][1] not in visited
                heapq.heapify(neighbors_list)
                print('neighbors: ', neighbors_list)
                heapq.heappush(queue, neighbors_list)
                x+=1

mst_graph = Graph('./data/small.csv').construct_mst()