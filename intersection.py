#This module is used for determining whether any of the lines in the game intersect with objects.
#This module has mostly been worked on by Christian.

import numpy as np
import math
from grid import Grid
import pygame

def subtract(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    return (x1 - x2, y1 - y2)

# take the cross product of 2 vectors, here p1 and p2 are vectors
def cross_product(p1, p2):
    x1, x2 = p1
    y1, y2 = p2
    return float(x1 * y2 - x2 * y1)

# Here p1, p2 are start and end point of a line, and p3 is a point from another line
def direction(p1, p2, p3):
    return cross_product(subtract(p3, p1), subtract(p2, p1))

# Checks if p3 is between p1 and p2, where p1 and p2 make up a line.
def on_segment(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return min(x1, x2) <= x3 <= max(x1, x2) and min(y1, y2) <= y3 <= max(y1, y2)

# Check for intersection between two lines. P1 and p2 make up the first line, p3 and p4 make up the 2nd line.
def intersect(p1, p2, p3, p4):
    direct1 = direction(p3, p4, p1)
    direct2 = direction(p3, p4, p2)
    direct3 = direction(p1, p2, p3)
    direct4 = direction(p1, p2, p4)

    # If this boolean holds, the lines are crossing eachother.
    if ((direct1 > 0 and direct2 < 0) or (direct1 < 0 and direct2 > 0)) and ((direct3 > 0 and direct4 < 0) or (direct3 < 0 and direct4 > 0)):
        return True

    # If either of these booleans hold, a point is laying on a line.
    elif direct1 == 0 and on_segment(p3, p4, p1):
        return True
    elif direct2 == 0 and on_segment(p3, p4, p2):
        return True
    elif direct3 == 0 and on_segment(p1, p2, p3):
        return True
    elif direct4 == 0 and on_segment(p1, p2, p4):
        return True
    else:
        return False

# Checks for collision between the newly drawn line and all other lines on the screen
def other_collision(tempLst, permLst):
    collision_bool = False

    # Outer loop iterates the temporary list (newly drawn line)
    curr_segment = tempLst.head
    while curr_segment:
        # Inner loop iterates the permanent list
        curr_permLst = permLst.head
        while curr_permLst:
            if (intersect(curr_segment.data[0], curr_segment.data[1], curr_permLst.data[0], curr_permLst.data[1])):
                print("Collision with other line")
                collision_bool = True
                return collision_bool
            curr_permLst = curr_permLst.next
        curr_segment = curr_segment.next
    return collision_bool

# Checks for collision between the newly drawn line and itself
def self_collision(tempLst):
    collision_bool = False
    # Outer loop iterates the temporary list (newly drawn line)
    curr_segment = tempLst.head
    while curr_segment:
        # Inner loop iterates all items coming after the one the outer loop is at (newly drawn line)
        curr_tempLst2 = curr_segment.next
        while curr_tempLst2:
            # Skip if the two lines are in succesion
            if (curr_segment.next == curr_tempLst2):
                curr_tempLst2 = curr_tempLst2.next
                continue
            elif (intersect(curr_segment.data[0], curr_segment.data[1], curr_tempLst2.data[0], curr_tempLst2.data[1])):
                print("COLLISION ")
                collision_bool = True
                return collision_bool
            curr_tempLst2 = curr_tempLst2.next
        curr_segment = curr_segment.next
    return collision_bool

# There's a collision if either there's a collision with the newly drawn line and other line or the newly drawn line itself
def collision(tempLst, permLst):
    return other_collision(tempLst, permLst) or self_collision(tempLst)

# If a line has been drawn through a node it will be disconnected
# Check to see if a line is disconnected
def disconnected(tempLst):
    notConnected = False
    
    #Iterate through the list
    curr_segment = tempLst.head
    while curr_segment:
        # If there's no pointer then a disconnection has been found in the previous iteration
        if (curr_segment.next == None):
            return notConnected
        curr_next_segment = curr_segment.next
        
        # If the end point of the current node doesn't equal the start point of the next node, they're disconnected
        if not (curr_segment.data[0] == curr_next_segment.data[1]):
            notConnected = True
            return notConnected
        curr_segment = curr_segment.next
    return notConnected

# Calculate the metric distance between two points
def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return float(math.sqrt((x2-x1)**2+(y2-y1)**2))
    
# Find the closest point on the newly drawn line to the mouse click
def closest_point(mouse_pos, lst, startNode, endNode, nodeSize, permLst, spritesLst, display):
    radius = 30 # Determine the minimum distance from start/end node to the new node

    center_startNode = np.subtract(startNode.getCoordinates(), (nodeSize/2, nodeSize/2))
    center_endNode = np.subtract(endNode.getCoordinates(), (nodeSize/2, nodeSize/2))

    # If this is true, the point on the line is far enough away from the start and end node
    Node_bool = False

    shortestDist = 999999999 #Through every iteration it will try to look for a shorter distance

    # Iterate through the newly drawn line
    curr_segment = lst.head
    closestNode = curr_segment.data[0]
    while curr_segment:
        # Find the distance between the current points start node on the line and the start/end node
        dx_end = abs(curr_segment.data[0][0] - endNode.rect.x-10)
        dy_end = abs(curr_segment.data[0][1] - endNode.rect.y-10)
        dx_start = abs(curr_segment.data[0][0] - startNode.rect.x-10)
        dy_start = abs(curr_segment.data[0][1] - startNode.rect.y-10)

        # Check if the point on the line is far enough away from the start/end node
        if (distance(mouse_pos, center_startNode) >= distance(mouse_pos, center_endNode)):
            if (dx_end>radius or dy_end>radius):
                Node_bool = True
            else:
                Node_bool = False
        elif(distance(mouse_pos, center_startNode) < distance(mouse_pos, center_endNode)):
            if (dx_start>radius or dy_start>radius):
                Node_bool = True
            else:
                Node_bool = False

        # Distance between the mouse click and the start point of the current line
        distance_from_click = distance(curr_segment.data[0], mouse_pos)
        # If the distance is shorter and it's out of range of the start/end node, update the shortest distance and closest point on the line
        if(distance_from_click <= shortestDist and Node_bool):
            if (intersectionWithOtherPoints(curr_segment.data[0], spritesLst, display)):
                shortestDist = distance_from_click
                closestNode = curr_segment.data[0]
        curr_segment = curr_segment.next
    if(closestNode == lst.head.data[0]):
        print("No point found")
    return closestNode

# Check if the new point is close to another node in the game which is not the start/end point of the new line
def intersectionWithOtherPoints(pointOnLine, spritesLst, display):
    newPoint = pygame.draw.circle(display.screen, display.WHITE, (pointOnLine[0], pointOnLine[1]), 7)
    for sprite in spritesLst:
        if (sprite.rect.colliderect(newPoint)):
            print("Too close to a node")
            return False
            break
        else:
            continue
    return True
