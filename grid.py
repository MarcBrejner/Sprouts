#This class is represents the underlying grid-graph used in the game for suggesting a path to the user.
#It has mostly been worked on by Marc

import networkx as nx
import numpy as np
import pygame
import intersection
import copy
from itertools import product

class Grid():
    def __init__(self, width, height):
        #Initialize grid-graph using NetworkX
        self.G = nx.grid_2d_graph(width,height)

    #Produces the set of integer-points (x,y) inside the circle with radius and x0,y0 as center.
    #The method is a modified version of the one found in https://stackoverflow.com/questions/49551440/python-all-points-on-circle-given-radius-and-center
    def points_in_circle_np(radius, x0=0, y0=0, ):
        s = set()
        x_ = np.arange(x0 - radius - 1, x0 + radius + 1, dtype=int)
        y_ = np.arange(y0 - radius - 1, y0 + radius + 1, dtype=int)
        x, y = np.where((x_[:,np.newaxis] - x0)**2 + (y_ - y0)**2 <= radius**2)
        for x, y in zip(x_[x], y_[y]):
            s.add((x,y))
        return s


    def block_nodes(lst,Gr,startNode,endNode,placedNode=None,reverseMargin=0): #Removes vertices from the input grid if they are near the line represented by the input lst
        head = lst.head
        radius = 5

        while head:
            xStart,yStart = head.data[0]
            xEnd,yEnd = head.data[1]
            if not (Grid.isPointInAnyCircle(startNode,endNode,placedNode,xStart,yStart)):
                Gr.G.remove_nodes_from(Grid.points_in_circle_np(radius,xStart,yStart))
            if not (Grid.isPointInAnyCircle(startNode,endNode,placedNode,xEnd,yEnd)):
                Gr.G.remove_nodes_from(Grid.points_in_circle_np(radius,xEnd,yEnd))
            head = head.next

    def find_path(startNode, endNode , lst , G , spriteList):

        #Coordinate-position of the source
        startPos = ((startNode.rect.centerx),(startNode.rect.centery))

        #Coordinate-position of the terminal
        endPos = ((endNode.rect.centerx),(endNode.rect.centery))

        #Make a copy of the grid, but with blocked areas around secondary nodes
        H = Grid.pruned_grid(startNode , endNode , G , 5 , spriteList)

        #try to find shortest path using NetworkX's implementation of Dijkstra's shortest path algorithm
        try:
            path = nx.dijkstra_path(H,startPos,endPos)
        except:
            raise Exception("No path available")
            return
        last_point = startPos
        #insert path in the format of line-segments into the input linked list
        for point in path:
            lst.prepend((last_point,point))
            last_point = point

    
    def remove_node_area(node,Gr,margin): #Removes underlying grid in a circle around a given node, with customizable margin
        Gr.G.remove_nodes_from(Grid.points_in_circle_np(node.radius+margin,node.rect.centerx,node.rect.centery))

    def pruned_grid(start,end,Gr,margin,spriteList): #Creates a copy of the input grid, and removes vertices in the areas around secondary nodes.
        H = Gr.G.__class__()
        H.add_nodes_from(Gr.G)
        H.add_edges_from(Gr.G.edges)
        for sprite in spriteList:
            if not ((sprite == start) or (sprite == end)):
                H.remove_nodes_from(Grid.points_in_circle_np(sprite.radius+margin,sprite.rect.centerx,sprite.rect.centery))
        return H

    def set_of_circumfering_points(node,Gr): #Finds the set of points that lies in circumference of a node, currently not in use
        margin = 1
        #set of points on node
        Q = Grid.points_in_circle_np(node.radius,node.rect.centerx,node.rect.centery)

        #set of points around node
        W = Grid.points_in_circle_np(node.radius+margin,node.rect.centerx,node.rect.centery)

        #remove Q from W
        W.difference_update(Q)
        W.intersection_update(Gr.G.nodes)
        return W

    def isPointInCircle(center_x, center_y, radius, x, y): #Returns a boolean reflecting whether or not a given point, lies within a given circle.
        dist = abs(x - center_x)**2 + abs(y - center_y)**2
        return dist < radius **2

    def isPointInAnyCircle(node1,node2,placedNode,x,y): #Returns a boolean reflecting whether or not a given point, lies within any of the three given nodes.
        if Grid.isPointInCircle(node1.rect.centerx,node1.rect.centery,node1.radius,x,y):
           return True
        elif Grid.isPointInCircle(node2.rect.centerx,node2.rect.centery,node2.radius,x,y):
           return True
        elif not (placedNode == None):
           if Grid.isPointInCircle(placedNode.rect.centerx,placedNode.rect.centery,placedNode.radius,x,y):
                return True
        else: 
           return False