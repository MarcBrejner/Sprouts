import networkx as nx
import numpy as np
from itertools import product

class Grid():
    def __init__(self, width, height):
        #G = nx.grid_2d_graph(self.disp.size[0],self.disp.size[1])
        self.G = nx.grid_2d_graph(width,height)

    #https://stackoverflow.com/questions/49551440/python-all-points-on-circle-given-radius-and-center
    def points_in_circle_np(radius, x0=0, y0=0, ):
        s = set()
        x_ = np.arange(x0 - radius - 1, x0 + radius + 1, dtype=int)
        y_ = np.arange(y0 - radius - 1, y0 + radius + 1, dtype=int)
        x, y = np.where((x_[:,np.newaxis] - x0)**2 + (y_ - y0)**2 <= radius**2)
        # x, y = np.where((np.hypot((x_-x0)[:,np.newaxis], y_-y0)<= radius)) # alternative implementation
        for x, y in zip(x_[x], y_[y]):
            s.add((x,y))
        return s

    
    def points_in_circle(radius):
        for x, y in product(range(int(radius) + 1), repeat=2):
            if x**2 + y**2 <= radius**2:
                yield from set(((x, y), (x, -y), (-x, y), (-x, -y),))
    

    def block_nodes(lst,Gr):
        head = lst.head
        while head:
            #We only use the start point of a segment because the circle is big enough
            x,y = head.data[0]
            Gr.G.remove_nodes_from(Grid.points_in_circle_np(3,x,y))
            head = head.next

    def find_path(start,end,lst,Gr):
        try:
           path = nx.dijkstra_path(Gr.G,start,end)
        except:
           print("Path not available")
           return
        last_point = start
        for point in path:
            lst.prepend((last_point,point))
            last_point = point

        
        #Q = Grid.points_in_circle_np(5,6,6)
        #print("nodes in Q")
        #print(list(Q))

        #G.remove_nodes_from(Q)
        #print("nodes after")
        #print(list(G.nodes))

        #print(nx.dijkstra_path(G,(1,1),(5,5)))

    
