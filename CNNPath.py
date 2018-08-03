import sys
import Tkinter as tk
import time  # sleep
import threading
import Queue
from HamsterAPI.comm_ble import RobotComm
import logging
from mr_grid_graph import GridGraph
from starter_bfs import BFS
from starter_grid_graph import SimpleGridGraph

class GUI(object):
    def __init__(self, root, robotList):
        self.root = root
        self.robotList = robotList  # handle to robot commands
        self.canvas = None
        self.node_dist = 60
        self.node_size = 20
        self.initUI()

    def initUI(self):
        self.canvas = tk.Canvas(self.root, bg = 'gray', width = 1440, height = 790)
        self.canvas.pack()

        self.b1 = tk.Button(self.root, text='Scan Image', height = 100, width = 10)
        self.b1.pack(side='left')
        self.b1.bind('<Button-1>', self.scanImage)

        self.b4 = tk.Button(self.root, text='Draw Grid', height = 100, width = 10)
        self.b4.pack(side='left')
        self.b4.bind('<Button-1>', self.drawGrid)

        self.b2 = tk.Button(self.root, text='Plan Path', height = 100, width = 10)
        self.b2.pack(side='left')
        self.b2.bind('<Button-1>', self.planPath)

        self.b3 = tk.Button(self.root, text='Execute Path', height = 100, width = 10)
        self.b3.pack(side='left')
        self.b3.bind('<Button-1>', self.executePath)

        self.b5 = tk.Button(self.root, text='Exit', height = 100, width = 10)
        self.b5.pack(side='right')
        self.b5.bind('<Button-1>', self.stopProg)

    def scanImage(self, event = None):
        self.img = None
        if self.img:
            self.canvas.create_image(1420,20, anchor=tk.NE, image=self.img)
        else:
            self.img = tk.PhotoImage(file="photo.gif")
            self.canvas.create_image(1420,20, anchor=tk.NE, image= self.img)

    def drawGrid(self, event = None):
        self.graph = GridGraph()
        self.graph.set_grid_rows(3)
        self.graph.set_grid_cols(3)

        self.start_node = '1-0-1-1'
        self.goal_node = '1-1-1-0'

        self.graph.obs_list = ([0,0],[0,1],[2,0],[2,1])

        self.graph.set_start(self.start_node)
        self.graph.set_goal(self.goal_node)

        self.graph.make_grid()
        self.graph.connect_nodes()

        self.display_graph()


    def planPath(self, event = None):
        bfs = BFS(self.graph)
        path = bfs.bfs_shortest_path(self.start_node,self.goal_node)

        path1 = [item[0:3] for item in path]
        path2 = [item[4:7] for item in path]

        self.actions1 = self.plan_path(path1)
        self.actions2 = self.plan_path(path2)

        #highlight path too
        self.highlight_path(path1, "cyan")
        self.highlight_path(path2, "yellow")

        print path1
        print path2

        print self.actions1
        print self.actions2

    def executePath(self, event = None):
        t1 = threading.Thread(name = "Actions 1 Execution", target = self.execute_path, args = (self.actions1,1))
        t1.setDaemon(True)
        t1.start()

        t2 = threading.Thread(name = "Actions 2 Execution", target = self.execute_path, args = (self.actions2,2))
        t2.setDaemon(True)
        t2.start()

    def stopProg(self, event = None):
        for robot in self.robotList:
            robot.reset()
        self.root.quit()    # close GUI window

    def display_graph(self):
        temp_graph = SimpleGridGraph()

        temp_graph.set_grid_rows(3)
        temp_graph.set_grid_cols(3)

        # origin of grid is (0, 0) lower left corner
        # graph.obs_list = ([1,1],)    # in case of one obs. COMMA
        temp_graph.obs_list = self.graph.obs_list = ([0,0],[0,1],[2,0],[2,1])
        
        temp_graph.make_grid()
        temp_graph.connect_nodes()
        temp_graph.compute_node_locations()

        temp_graph_nodes_location = temp_graph.node_display_locations

        for node1,l in temp_graph.nodes.iteritems():
            for node2 in l:
                self.draw_edge(node1,node2,"black")  
        for nodeX,nodeY,name in temp_graph_nodes_location:
            if ([int(name.split("-")[0]),int(name.split("-")[1])] in temp_graph.obs_list):
                self.draw_node(nodeX,nodeY,name, "red")
            else:
                self.draw_node(nodeX,nodeY,name, "white")

    # path is a list of nodes ordered from start to go2al node
    def highlight_path(self, path, color):
        for i in range(1,len(path)):
            self.draw_edge(list(path)[i-1],list(path)[i],color)  

        for name in path:
            nodeX = int(name.split('-')[1])+1
            nodeY = self.graph.grid_rows - int(name.split('-')[0])
            self.draw_node(nodeX,nodeY,name, color)
  
    # draws a node in given color. The node location info is in passed-in node object
    def draw_node(self, nodeX,nodeY,name, n_color):
        self.canvas.create_oval(nodeX*self.node_dist-self.node_size,nodeY*self.node_dist-self.node_size,nodeX*self.node_dist+self.node_size,nodeY*self.node_dist+self.node_size,fill = n_color)
        self.canvas.create_text(nodeX*self.node_dist,nodeY*self.node_dist,fill="black", text=name)

    # draws an line segment, between two given nodes, in given color
    def draw_edge(self, node1, node2, e_color):
        node1X = (int(node1.split('-')[1])+1) * self.node_dist
        node1Y = (self.graph.grid_rows - int(node1.split('-')[0])) * self.node_dist

        node2X = (int(node2.split('-')[1])+1) * self.node_dist
        node2Y = (self.graph.grid_rows - int(node2.split('-')[0])) * self.node_dist

        self.canvas.create_line(node1X, node1Y, node2X, node2Y,fill = e_color, width = 4)

    def plan_path(self, path):
        planned_path = []
        plan = []
        
        for i in range(1,len(path)):
            node1X = (int(path[i-1].split('-')[1]))
            node1Y = (int(path[i-1].split('-')[0]))

            node2X = (int(path[i].split('-')[1]))
            node2Y = (int(path[i].split('-')[0]))

            if (node2X>node1X):
                plan.append("r")
            elif (node2X<node1X):
                plan.append("l")
            elif (node2Y>node1Y):
                plan.append("u")
            elif (node2Y<node1Y):
                plan.append("d")
        
        print plan
        
        prev = 'u'
        for direction in plan:
            if prev == direction:
                planned_path.append('f')
            elif prev == 'u' and direction == 'r':
                planned_path.append('r')
                planned_path.append('f')
            elif prev == 'u' and direction == 'l':
                planned_path.append('l')
                planned_path.append('f')
            elif prev == 'u' and direction == 'd':
                planned_path.append('l')
                planned_path.append('l')
                planned_path.append('f')
            elif prev == 'd' and direction == 'u':
                planned_path.append('r')
                planned_path.append('r')
                planned_path.append('f')
            elif prev == 'd' and direction == 'r':
                planned_path.append('l')
                planned_path.append('f')
            elif prev == 'd' and direction == 'l':
                planned_path.append('r')
                planned_path.append('f')
            elif prev == 'l' and direction == 'u':
                planned_path.append('r')
                planned_path.append('f')
            elif prev == 'l' and direction == 'd':
                planned_path.append('l')
                planned_path.append('f')
            elif prev == 'l' and direction == 'r':
                planned_path.append('l')
                planned_path.append('l')
                planned_path.append('f')
            elif prev == 'r' and direction == 'u':
                planned_path.append('l')
                planned_path.append('f')
            elif prev == 'r' and direction == 'd':
                planned_path.append('r')
                planned_path.append('f')
            elif prev == 'r' and direction == 'l':
                planned_path.append('l')
                planned_path.append('l')
                planned_path.append('f')
            elif prev == None:
                planned_path.append('f')
            prev = direction
        return planned_path

    def execute_path(self, actions, index):
        while len(actions)>0:
            if self.robotList:
                self.robotList[index-1].set_led(0,index*3)
                self.robotList[index-1].set_led(1,index*3)
                command = actions.pop(0)
                if command == 'f':
                    self.move_f(index)
                elif command == 'l':
                    self.turn_l(index)
                elif command == 'r':
                    self.turn_r(index)

    def move_f(self, index):
        #print "move_f"
        robot = self.robotList[index-1]

        robot.set_wheel(0,20)
        robot.set_wheel(1,20)
        time.sleep(0.1)

        while (robot.get_floor(0) > 50 or robot.get_floor(1) > 50):
            if robot.get_floor(0) < 20:
                robot.set_wheel(0,8)
                robot.set_wheel(1,20)
                time.sleep(0.05)
            elif robot.get_floor(1) < 20:
                robot.set_wheel(0,20)
                robot.set_wheel(1,8)
                time.sleep(0.05)
            else:
                robot.set_wheel(0,20)
                robot.set_wheel(1,20)
                time.sleep(0.01)

        robot.set_musical_note(40)
        time.sleep(0.7)
        robot.set_musical_note(0)
        robot.set_wheel(0,0)
        robot.set_wheel(1,0)

    def turn_l(self, index):
        #print "turn_l"
        robot = self.robotList[index-1]
        robot.set_wheel(0,-30)
        robot.set_wheel(1,30)
        time.sleep(0.8)
        robot.set_wheel(0,30)
        robot.set_wheel(1,30)
        time.sleep(0.1)
        robot.set_wheel(0,0)
        robot.set_wheel(1,0)

    def turn_r(self, index):
        #print "turn_r"
        robot = self.robotList[index-1]
        robot.set_wheel(0,30)
        robot.set_wheel(1,-30)
        time.sleep(0.8)
        robot.set_wheel(0,30)
        robot.set_wheel(1,30)
        time.sleep(0.1)
        robot.set_wheel(0,0)
        robot.set_wheel(1,0)

def main():
    max_robot_num = 2   # max number of robots to control
    comm = RobotComm(max_robot_num)
    comm.start()
    print 'Bluetooth starts'
    robotList = comm.robotList

    root = tk.Tk()
    root.geometry('1440x900')

    ui = GUI(root, robotList)

    root.mainloop()

if __name__ == "__main__":
    main()
    sys.exit()