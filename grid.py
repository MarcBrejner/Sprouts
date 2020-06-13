import networkx as nx
import numpy as np
import pygame
import intersection
import copy
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
            radius = 5
            x,y = head.data[0]
            Gr.G.remove_nodes_from(Grid.points_in_circle_np(radius,x,y))
            head = head.next

    def find_path(start,end,lst,G):
        try:
            path = nx.dijkstra_path(G,start,end)
        except:
            print("Path not available")
            return
        last_point = start
        for point in path:
            lst.prepend((last_point,point))
            last_point = point

    def remove_node_area(node,Gr,margin):
        Gr.G.remove_nodes_from(Grid.points_in_circle_np(node.radius+margin,node.rect.centerx,node.rect.centery))

    def add_node_area(node,Gr): #obsolete
        margin = 5
        Q = Grid.points_in_circle_np(node.radius,node.rect.centerx,node.rect.centery)
        #set of points around node
        W = Grid.points_in_circle_np(node.radius+margin,node.rect.centerx,node.rect.centery)
        W.difference_update(Q)
        Gr.G.add_nodes_from(W)

    def pruned_grid(start,end,Gr,margin,spriteList):
        H = Gr.G.__class__()
        H.add_nodes_from(Gr.G)
        H.add_edges_from(Gr.G.edges)
        for sprite in spriteList:
            if not ((sprite == start) or (sprite == end)):
                H.remove_nodes_from(Grid.points_in_circle_np(sprite.radius+margin,sprite.rect.centerx,sprite.rect.centery))
        return H

    def set_of_circumfering_points(node,Gr):
        margin = 2
        #set of points on node
        Q = Grid.points_in_circle_np(node.radius,node.rect.centerx,node.rect.centery)

        #set of points around node
        W = Grid.points_in_circle_np(node.radius+margin,node.rect.centerx,node.rect.centery)

        #remove Q from W
        W.difference_update(Q)
        W.intersection_update(Gr.G.nodes)
        return W

    def closest_in_set(mouse_pos,set):
        shortestDist = 9999
        point = mouse_pos
        for p in set:
            dist = intersection.distance(mouse_pos,p)
            if dist < shortestDist:
                shortestDist = dist
                point = p
        return point
            

        
        #Q = Grid.points_in_circle_np(5,6,6)
        #print("nodes in Q")
        #print(list(Q))

        #G.remove_nodes_from(Q)
        #print("nodes after")
        #print(list(G.nodes))

        #print(nx.dijkstra_path(G,(1,1),(5,5)))

    
