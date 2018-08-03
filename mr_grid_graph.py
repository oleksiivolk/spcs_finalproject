import Tkinter as tk
from starter_bfs import BFS

class GridGraph(object):
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
        x1 = int(name.split("-")[0])
        y1 = int(name.split("-")[1])
        x2 = int(name.split("-")[2])
        y2 = int(name.split("-")[3])

        if ((x1,y1) != (x2,y2)):
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

        if len(node2.split("-")) != 4:
            return
        # x/y    node num     robot num
        x11 = int(node1.split("-")[0])
        y11 = int(node1.split("-")[1])
        x12 = int(node1.split("-")[2])
        y12 = int(node1.split("-")[3])
        x21 = int(node2.split("-")[0])
        y21 = int(node2.split("-")[1])
        x22 = int(node2.split("-")[2])
        y22 = int(node2.split("-")[3])

        

        if (('None' not in node1)
        and ('None' not in node2)
        and ([x11,y11] not in self.obs_list) 
        and ([x12,y12] not in self.obs_list)
        and ([x21,y21] not in self.obs_list) 
        and ([x22,y22] not in self.obs_list)
        and (x11 < self.grid_rows and x11 >= 0)
        and (x12 < self.grid_rows and x12 >= 0)
        and (x21 < self.grid_rows and x21 >= 0)
        and (x22 < self.grid_rows and x22 >= 0)
        and (y11 < self.grid_columns and y11 >= 0)
        and (y12 < self.grid_columns and y12 >= 0)
        and (y21 < self.grid_columns and y12 >= 0)
        and (y22 < self.grid_columns and y22 >= 0)
        and (x11,y11) != (x12,y12)
        and (x21,y21) != (x22,y22)
        and self.adjacent(x11,y11,x21,y21)
        and self.adjacent(x12,y12,x22,y22)
        and not ((x11,y11)==(x22,y22) and (x21,y21)==(x12,y12))):
            self.nodes[node1].add(node2)
            self.nodes[node2].add(node1)

    # populate graph with all the nodes in the graph, excluding obstacle nodes
    def make_grid(self):
        for x1 in range(self.grid_rows):
            for y1 in range(self.grid_columns):
                for x2 in range(self.grid_rows):
                    for y2 in range(self.grid_columns):
                        self.add_node(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2))

    def adjacent(self, x1, y1, x2, y2):
        if abs(x1-x2) < 2 and abs(y1-y2) < 2:
            return True
        else:
            return False

    # Based on node's name, this method identifies its neighbors and fills the 
    # set holding neighbors for every node in the graph.
    def connect_nodes(self):
        for x1 in range(self.grid_rows):
            for y1 in range(self.grid_columns):
                for x2 in range(self.grid_rows):
                    for y2 in range(self.grid_columns):
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1-1)+"-"+str(y1)+"-" +str(x2-1)+"-"+str(y2))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1-1)+"-"+str(y1)+"-" +str(x2+1)+"-"+str(y2))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1-1)+"-"+str(y1)+"-" +str(x2)+"-"+str(y2-1))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1-1)+"-"+str(y1)+"-" +str(x2)+"-"+str(y2+1))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1-1)+"-"+str(y1)+"-" +str(x2)+"-"+str(y2))

                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1+1)+"-"+str(y1)+"-" +str(x2-1)+"-"+str(y2))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1+1)+"-"+str(y1)+"-" +str(x2+1)+"-"+str(y2))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1+1)+"-"+str(y1)+"-" +str(x2)+"-"+str(y2-1))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1+1)+"-"+str(y1)+"-" +str(x2)+"-"+str(y2+1))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1+1)+"-"+str(y1)+"-" +str(x2)+"-"+str(y2))


                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1-1)+"-" +str(x2-1)+"-"+str(y2))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1-1)+"-" +str(x2+1)+"-"+str(y2))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1-1)+"-" +str(x2)+"-"+str(y2-1))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1-1)+"-" +str(x2)+"-"+str(y2+1))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1-1)+"-" +str(x2)+"-"+str(y2))

                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1+1)+"-" +str(x2-1)+"-"+str(y2))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1+1)+"-" +str(x2+1)+"-"+str(y2))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1+1)+"-" +str(x2)+"-"+str(y2-1))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1+1)+"-" +str(x2)+"-"+str(y2+1))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1+1)+"-" +str(x2)+"-"+str(y2))


                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1)+"-" +str(x2-1)+"-"+str(y2))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1)+"-" +str(x2+1)+"-"+str(y2))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1)+"-" +str(x2)+"-"+str(y2-1))
                        self.add_neighbor(str(x1)+"-"+str(y1)+"-"+str(x2)+"-"+str(y2), str(x1)+"-"+str(y1)+"-" +str(x2)+"-"+str(y2+1))




###########################################################
#  A testing program of your implementaion of GridGraph class.
###########################################################
def main():
    graph = GridGraph()
    # grid dimension
    graph.set_grid_rows(4)
    graph.set_grid_cols(4)

    # origin of grid is (0, 0) lower left corner
    # graph.obs_list = ([1,1],)    # in case of one obs. COMMA
    graph.obs_list = [[1,0], [3,0], [2,1]]
    
    graph.set_start('0-0-1-1')
    graph.set_goal('2-2-3-3')
    
    graph.make_grid()
    graph.connect_nodes()

    bfs = BFS(graph)
    path = bfs.bfs_shortest_path('0-0-1-1','2-2-3-3')

    print path

    return

if __name__ == "__main__":
    main()