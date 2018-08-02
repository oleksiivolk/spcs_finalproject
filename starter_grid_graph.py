'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          grid_graph_starter.py
   By:            Qin Chen
   Last Updated:  6/10/18
    
   Definition of class GridGraph. Description of all the methods is
   provided. Students are expected to implement the methods for Lab#6.
   ========================================================================*/
'''
import Tkinter as tk

class SimpleGridGraph(object):
    def __init__(self):
        self.nodes = {} # {node_name: set(neighboring nodes), ...}
        self.startNode = None  # string
        self.goalNode = None    # string
        self.grid_rows = None
        self.grid_columns = None
        self.obs_list = []
        self.node_display_locations=[]
        return

    # set number of rows in the grid
    def set_grid_rows(self, rows):
        self.grid_rows = rows

    # set number of columns in the grid
    def set_grid_cols(self, cols):
        self.grid_columns = cols

    # this method is used by make_grid() to create a key-value pair in self.nodes{},
    # where value is created as an empty set which is populated later while connecting
    # nodes.
    def add_node(self, name):
        self.nodes[name] = set([])

    # set start node name
    def set_start(self, name):
        self.startNode = name

    # returns start node name
    def get_start_node(self):
        return self.startNode

    # set goal node name
    def set_goal(self, name):
        self.goalNode = name

    # return goal node name
    def get_goal_node(self):
        return self.goalNode

    # Given two neighboring nodes. Put them to each other's neighbors-set. This
    # method is called by self.connect_nodes() 
    def add_neighbor(self, node1, node2):
        if 'None' not in node1 and 'None' not in node2 and ([int(node1.split("-")[0]),int(node1.split("-")[1])] not in self.obs_list) and ([int(node2.split("-")[0]),int(node2.split("-")[1])] not in self.obs_list):
            self.nodes[node1].add(node2)
            self.nodes[node2].add(node1)

    # populate graph with all the nodes in the graph, excluding obstacle nodes
    def make_grid(self):
        for i in range(self.grid_rows):
            for j in range(self.grid_columns):
                self.add_node(str(i)+ "-" + str(j))

    def not_out(self, num, n):
        if num < 0:
            return None
        elif num >= n:
            return None
        else:
            return num

    # Based on node's name, this method identifies its neighbors and fills the 
    # set holding neighbors for every node in the graph.
    def connect_nodes(self):
        for i in range(self.grid_rows):
            for j in range(self.grid_columns):
                self.add_neighbor(
                    str(self.not_out(i-1,self.grid_rows))+ "-" + str(self.not_out(j,self.grid_columns)),
                    str(i) + "-" + str(j)
                    )
                self.add_neighbor(
                    str(self.not_out(i+1,self.grid_rows))+ "-" + str(self.not_out(j,self.grid_columns)),
                    str(i) + "-" + str(j)
                    )
                self.add_neighbor(
                    str(self.not_out(i,self.grid_rows))+ "-" + str(self.not_out(j-1,self.grid_columns)),
                    str(i) + "-" + str(j)
                    )
                self.add_neighbor(
                    str(self.not_out(i,self.grid_rows))+ "-" + str(self.not_out(j+1,self.grid_columns)),
                    str(i) + "-" + str(j)
                    )



    # For display purpose, this function computes grid node location(i.e., offset from upper left corner where is (1,1)) 
    # of display area. based on node names.
    # Node '0-0' is displayed at bottom left corner 
    def compute_node_locations(self):
        nodeLocation = []
        for name in self.nodes:
            nodeX = int(name.split('-')[1])+1
            nodeY = self.grid_rows - int(name.split('-')[0])
            nodeLocation.append((nodeX,nodeY,name))
        self.node_display_locations = nodeLocation

###########################################################
#  A testing program of your implementaion of GridGraph class.
###########################################################
def main():
    graph = SimpleGridGraph()
    # grid dimension
    graph.set_grid_rows(4)
    graph.set_grid_cols(3)

    # origin of grid is (0, 0) lower left corner
    # graph.obs_list = ([1,1],)    # in case of one obs. COMMA
    graph.obs_list = ([1,1], [3,0], [2,2])
    
    graph.set_start('0-0')
    graph.set_goal('2-1')
    
    graph.make_grid()
    graph.connect_nodes()

    print graph.nodes

    return

if __name__ == "__main__":
    main()