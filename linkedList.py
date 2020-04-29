# Node class
class Node:

    # Initialize node
    def __init__(self, data=None, next=None):
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
    def remove(self):
        curr = self.head
        while curr:
            prev = curr.next
            del curr.data
            curr = prev
    



