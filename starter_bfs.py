'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          bfs_engine.py
   By:            Qin Chen
   Last Updated:  6/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import Queue

class BFS(object):
    def __init__(self, graph):  
        self.graph = graph
        return

    ######################################################
    # this function returns the shortest path for given start and goal nodes
    ######################################################
    def bfs_shortest_path(self, start, goal):
        paths = []
        paths.append((start,[start]))

        while paths:
            node, path = paths.pop(0)

            for next in self.graph.nodes[node] - set(path):
                if next == goal:
                    return path + [next]
                else:   
                    paths.append((next,path + [next]))


    ######################################################
    # this function returns all paths for given start and goal nodes
    ######################################################
    def bfs_paths(self, start, end_node):
        paths = []
        paths.append((start,[start]))

        out = []

        while paths:
            node, path = paths.pop(0)

            for next in self.graph[node] - set(path):
                    paths.append((next,path + [next]))
                    if (next == end_node):
                        out.append(path + [next])
        return out
                
    #########################################################
    # This function returns the shortest paths for given list of paths
    #########################################################
    def shortest(self, paths):
        short = len(paths[0])
        index = 0

        for i, path in enumerate(paths):
            if len(path) < short:
                print "dab"
                short = len(path)
                index = i

        return paths[index]



    def bfs(self, start):
        visited = []
        q = Queue.Queue();

        q.put(start)
        while (q.qsize()!=0):
            node = q.get()
            if (not node in visited):
                visited.append(node)
                for u in self.graph[node]:
                    q.put(u)
        return visited


def main():
    graph = {'A': set(['B', 'C']),
        'B': set(['A', 'C', 'D', 'E']),
        'C': set(['A', 'B', 'D', 'G']),
        'D': set(['B', 'C', 'E', 'G']),
        'E': set(['B', 'D', 'F', 'G']),
        'F': set(['E','G']),
        'G': set(['C', 'D', 'E', 'F'])}
    bfs = BFS(graph)
    start_node = 'A'
    end_node = 'G'

    p = bfs.bfs_shortest_path(start_node, end_node)
    print "\n++++++++++Shortest path from %s to %s: %s\n" % (start_node, end_node, p)
    
    #find all the paths returned by bfs_paths()
    paths = list(bfs.bfs_paths(start_node, end_node)) # [['A', 'C', 'F'], ['A', 'B', 'E', 'F']]
    print "\n==========paths from %s to %s: %s\n" % (start_node, end_node, paths)
    print len(paths)
    print "\n----------shortest path: %s\n" % bfs.shortest(paths)

    # order holds traverse order of the all the nodes
    order = bfs.bfs(start_node)
    print "\n##########traverse order:", order

if __name__ == "__main__":
    main()