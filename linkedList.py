import pygame
from point import Point

# Node class
class Node:

    # Initialize node
    def __init__(self, data, next):
        self.data = data
        self.next = next

    def __repr__(self):
        return repr(self.data)

# Singly linked list - containing node objects
# Optimization - Find en måde at slette listen på
class LinkedList:
    
    # Initialize linked list
    def __init__(self):
        self.head = None

    def __repr__(self):
        nodes = []
        curr = self.head
        while curr:
            nodes.append(repr(curr))
            curr = curr.next
        return '[' + ','.join(nodes) + ']'

    # Insert item in the beginning of the list
    def prepend(self, data):
        self.head = Node(data=data, next=self.head)

    # Remove the content of the list
    def clean(self):
        curr = self.head
        while curr:
            prev = curr.next
            del curr.data
            curr = prev
    
    # Draw the first element of the list
    def drawHead(self, image, color):
        curr = self.head
        pygame.draw.line(image, color, curr.data[0], curr.data[1], 2)
    
    # Draw the entire list
    def drawLst(self, image, color):
        curr = self.head
        while curr:
            pygame.draw.line(image, color, curr.data[0] , curr.data[1], 2)
            curr = curr.next

    # Concat two linked lists
    def concatLst(self, tempLst):
        curr = self.head
        while curr.next != None:
            curr = curr.next
        curr.next = tempLst
        return permLst

    def merge(self, tempLst):
        curr = tempLst.head
        while curr:
            self.prepend(curr.data)
            curr = curr.next

