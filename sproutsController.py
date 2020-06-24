#IMPORTS
import pygame, random
from pygame.locals import *
from node import Node
from linkedList import LinkedList
from intersection import *
from tkinter import *
import networkx as nx
import numpy as np
from grid import Grid
from itertools import product

#Nodes
 
# Add the node to the list of objects

labelCounter = 0        #The label of the newest node
nodeSize = 15           #Static size used to display nodes
LEFT = 1                #Number used by pygame to represent left mouse button
RIGHT = 3               #Number used by pygame to represent right mouse button
mouse_position = (0, 0) #The current position of the mouse
pathfinding = False     #Boolean representing whether the system is trying to find a path
pathFound = False       #Boolean representing whether the system has found a path
drawing = False         #Boolean representing whether the user is currently drawing
merged = False          #Boolean representing whether the tempLst has been merged with the permLst
last_pos = None         #The position of the mouse before moving
isInsideNode = True     #Won't draw lines while this is true
exitedNode = False      #Ignores clicking inside a node to increase it's degree
placeNewPoint = False   #Whether or not it is time to place a new point before continuing
playerOneName = "Player 1"
playerTwoName = "Player 2"
displayName = playerOneName

#Messages to display in the tooltip window at the bottom of the screen
instMsgClickNode = "Left click a node to draw, right click to suggest"
instMsgPlacePoint = "Left click to place a point"
instMsgFinishPath = "Right click on a node to finish suggested line"
instMsgSaveLine = "Hit [space] to confirm the line or [esc] to deny"
instMsgNoPathfind = "No path available"
instMsgNodeIsFull = "The node is full, click another"

displayInst = instMsgClickNode

class SproutsController:
    def __init__(self,pygame,disp):
        self.disp = disp
        self.pygame = pygame
        self.all_sprites_list = pygame.sprite.Group() #Contains all sprites, ie. nodes
        self.permLst = LinkedList() #The list of all accepted lines
        self.tempLst = LinkedList() #The list containing the segments of the line currently being modified/drawn
        self.fixList = LinkedList() #Small list fix the visual bug where sometimes the line had a small visual gap between itself and the connected node.


    
    def GameLoop(self):

        #FIELDS
        global nodeSize
        global labelCounter
        global LEFT
        global RIGHT
        global mouse_position
        global pathfinding
        global drawing
        global merged
        global last_pos
        global isInsideNode
        global exitedNode
        global placeNewPoint
        global playerOneName
        global playerTwoName
        global pathFound
        global displayName
        global displayInst
        global instMsgClickNode
        global instMsgFinishPath
        global instMsgPlacePoint
        global instMsgSaveLine

        #Set background to white
        self.disp.screen.fill(self.disp.WHITE)

        #Create grid object, ie. underlying grid-graph.
        G = Grid(self.disp.size[0],self.disp.size[1])

        #Set currently displayed name
        displayName = playerOneName

        #This will be a list that will contain all the sprites we intend to use in our game.
        all_sprites_list = pygame.sprite.Group()
        startNode = None

        carryOn = True
        clock=pygame.time.Clock()
 
        while carryOn:
                for event in pygame.event.get():
                    #Allows the user to close the window
                    if event.type==pygame.QUIT:
                        carryOn=False   
                    elif pathFound: #If a path has just been found, wait for the user to either accept or discard the found line.
                        keys = pygame.key.get_pressed()
                        if keys[K_SPACE]:
                            self.permLst.merge(self.tempLst)
                            pathFound = False
                            placeNewPoint = True
                            startNode.incrementCounter()
                            endNode.incrementCounter()
                            displayInst = instMsgPlacePoint
                        elif keys[K_ESCAPE]:
                            self.tempLst.drawLst(self.disp.screen,self.disp.WHITE)
                            self.tempLst = LinkedList()
                            pathFound = False
                            placeNewPoint = False
                            displayInst = instMsgClickNode
                    elif event.type == MOUSEBUTTONDOWN and event.button == RIGHT:
                        #When right mb is pressed, checks if mouse is over a node, if so save node for pathfinding.
                        pos = pygame.mouse.get_pos()
                        for sprite in self.all_sprites_list:
                            if sprite.rect.collidepoint(pos):
                                if (sprite.isFull()):
                                    print("Illegal move, node is full")
                                    displayInst = instMsgNodeIsFull
                                elif (placeNewPoint):    
                                    print("Place a new point, by left clicking")
                                elif pathfinding and not (sprite == startNode):
                                    
                                    print("TO") 

                                    #Terminal node
                                    endNode = sprite

                                    print(endNode.getCoordinates()) #debug
                                    print("FINDING PATH...")
                                    
                                    try: #Checks if there is a path
                                        Grid.find_path(startNode , endNode , self.tempLst , self.G , self.all_sprites_list) #Find path from prev. node to current node.
                                        displayInst = instMsgSaveLine
                                        pathFound = True
                                    except Exception as e:
                                        print(str(e))
                                        displayInst = instMsgNoPathfind

                                    #No longer pathfinding
                                    pathfinding = False
                                    H = None

                                    #Draw found path, if any, red
                                    self.tempLst.drawLst(self.disp.screen,self.disp.LIGHT_RED)      

                                else:
                                    #Source node
                                    startNode = sprite
                                    
                                    print("FROM")
                                    print(sprite.getCoordinates()) #debug

                                    pathfinding = True #Start pathfinding
                                    displayInst = instMsgFinishPath
                                    
                         
                    elif event.type == MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                        if (drawing): #If the mouse moves, and the user is currently drawing
                            pos = pygame.mouse.get_pos()
                            # Restrict the mouse from going into the top region of the window
                            convert = list(pos)
                            if convert[1] < 50:
                                convert[1] = 50
                            pos = tuple(convert)

                            # Restrict the mouse from going into the bottom region of the window
                            convert = list(pos)
                            if convert[1] > 450:
                                convert[1] = 450
                            pos = tuple(convert)

                            for sprite in self.all_sprites_list:
                                if sprite.rect.collidepoint(pos):
                                    isInsideNode = True
                                    break
                                else:
                                    isInsideNode = False
                                    exitedNode = True
                            # Add the new line to the linked list and draw the line
                            if last_pos is not None and not isInsideNode:
                                    # Draws a line between the current mouse position and the mouse position from the last frame
                                    self.tempLst.prepend((last_pos, pos))
                                    self.tempLst.drawHead(self.disp.screen, self.disp.LIME_GREEN)
                            last_pos = pos
                    elif event.type == MOUSEBUTTONUP and event.button == LEFT:
                        #When mouse is released, checks if mouse is over a node
                        pos = pygame.mouse.get_pos()
                        for sprite in self.all_sprites_list:
                            if sprite.rect.collidepoint(pos):
                                if (sprite.isFull() or (sprite == startNode and sprite.getCounter() >= 2)):
                                    print("Illegal move, node is full")
                                    displayInst = instMsgNodeIsFull
                                elif (collision(self.tempLst, self.permLst)):
                                    print("Collision with an edge detected")
                                elif (disconnected(self.tempLst)):
                                    print("Collision with a node detected")
                                elif exitedNode:

                                    #Add edge to perm list of edges.
                                    self.fixList.prepend( (self.tempLst.head.data[1] , (sprite.rect.centerx,sprite.rect.centery)) ) #fix visual bug
                                    self.permLst.merge(self.tempLst)
                                    merged = True

                                    endNode = sprite

                                    #increment degree of both nodes
                                    sprite.incrementCounter()
                                    startNode.incrementCounter()

                                    print(sprite.getCounter())
                                    placeNewPoint = True
                                    displayInst = instMsgPlacePoint
                        
                        if (not merged): # Delete drawn line if it didn't end in a sprite
                            self.tempLst.drawLst(self.disp.screen, self.disp.WHITE)
                            self.tempLst = LinkedList()
                        #Reset mouse position, tempList and drawing status on release.
                        mouse_position = (0, 0)
                        last_pos = None
                        drawing = False
                        merged = False
                        exitedNode = False
                    elif event.type == MOUSEBUTTONDOWN and event.button == LEFT:
                        #When mouse is pressed, checks if mouse is over a node, if so start drawing.
                        pos = pygame.mouse.get_pos()
                        if (placeNewPoint):
                            newNode = self.newPointOnLine(pos, startNode, endNode, nodeSize)
                            self.all_sprites_list.add(newNode)
                            Grid.block_nodes(self.tempLst,self.G,startNode,endNode,newNode)
                            startNode = None
                            endNode = None
                            self.tempLst = LinkedList()
                            displayInst = instMsgClickNode
                            if (displayName == playerOneName):
                                displayName = playerTwoName
                            else:
                                displayName = playerOneName
                        elif(pathfinding):
                            print("Finish path finding by right clicking on a node")
                        else:
                            for sprite in self.all_sprites_list:
                                if sprite.rect.collidepoint(pos):
                                    if (sprite.isFull()):
                                        print("Illegal move, node is full")
                                        displayInst = instMsgNodeIsFull
                                    else:
                                        #save pressed node
                                        startNode = sprite
                                        drawing = True
                                        exitedNode = False
                                        placeNewPoint = False
                
                #Update visuals
                self.all_sprites_list.update()

                self.permLst.drawLst(self.disp.screen, self.disp.LIME_GREEN)
                self.fixList.drawLst(self.disp.screen, self.disp.LIME_GREEN)

                self.disp.gameButton("Controls", 20, 0, 100, 50, self.disp.BLACK, self.disp.GREEN, drawing, self.showControls)
                self.disp.gameButton("Surrender", self.disp.size[0]-140, 0, 120, 50, self.disp.BLACK, self.disp.GREEN, drawing, self.chooseWinner)
        
                self.all_sprites_list.draw(self.disp.screen)

                self.disp.turnTracker(displayName)

                self.disp.turnInstructions(displayInst)

                self.disp.updateScreen(pygame)

                #Number of frames per secong e.g. 60
                clock.tick(120)
        #Quit game if gameloop is exited
        pygame.quit()

    def initializeGameState(self, filename): #Initializes the game state specified in the textfile "filename"
        self.G = Grid(self.disp.size[0],self.disp.size[1])
        margin = 100
        lineCounter = 0
        y = 1
        x = 1
        firstRead = False
        f = open(filename,"r")
        lines = f.readlines()
        for line in lines:
            lineCounter += 1
            if not(firstRead): #For the very first line of the file, initialize only n nodes in grid-like structure
                n = int(line)
                for labelCounter in range(1,n+1):
                    currNode = Node(self.disp.BROWN, nodeSize, nodeSize, (margin*x),(margin*y), 0, labelCounter)
                    self.all_sprites_list.add(currNode)
                    x+=1
                    if ((margin*x)) >= (self.disp.size[0]):
                        x = 1
                        y += 1
                firstRead = True
            else: #For the rest of the lines in the file, connect nodes as specified, in the given order, until an error is encountered.
                labels = line.split()
                startNode = self.all_sprites_list.sprites()[int(labels[0])-1]
                endNode = self.all_sprites_list.sprites()[int(labels[1])-1]
                if startNode.isFull() or endNode.isFull(): #Check if a move would exceed the allowed maximum degree
                    print("Line {} would cause a node to exceed degree 3".format(lineCounter))
                    startNode = None
                    endNode = None
                    self.tempLst = LinkedList()
                    break;
                elif (labels[0] == labels[1]): #Check if a move asks for a loop, loops are allowed but the pathfinding algorithm can not handle it.
                    print("Loop detected at line {}, ending initialization".format(lineCounter))
                    startNode = None
                    endNode = None
                    self.tempLst = LinkedList()
                    break;
                try:
                    Grid.find_path(startNode,endNode,self.tempLst,self.G,self.all_sprites_list) #Try to find a path between the specified nodes.
                except:
                    print("Could not find a path between nodes {} and {} at line {} of initalize.txt..".format(labels[0],labels[1],lineCounter))
                    startNode = None
                    endNode = None
                    self.tempLst = LinkedList()
                    break;
                    
                #Place a new node on the found line, increment degrees, block nodes in the underlying grid, before moving on to the next line
                newNode = self.generate_node_on_path(startNode,endNode,self.tempLst,self.G)
                startNode.incrementCounter()
                endNode.incrementCounter()
                self.all_sprites_list.add(newNode)
                #Grid.remove_node_area(newNode,self.G,0)
                Grid.block_nodes(self.tempLst,self.G,startNode,endNode,newNode)

                self.permLst.merge(self.tempLst)
                startNode = None
                endNode = None
                self.tempLst = LinkedList()
        #Initialization finished
        print("Done with initialization")

    def newPointOnLine(self, pos, startNode, endNode, nodeSize):
        global labelCounter
        global placeNewPoint
        position_of_new_sprite = closest_point(pos, self.tempLst, startNode, endNode, nodeSize, self.permLst, self.all_sprites_list, self.disp)
        #self.all_sprites_list.add()
        newNode = Node(self.disp.BROWN, nodeSize, nodeSize, position_of_new_sprite[0], position_of_new_sprite[1], 2, labelCounter)
        labelCounter += 1
        placeNewPoint = False
        return newNode

    def generate_node_on_path(self,startNode,endNode,lst,G):
        radius = 30
        center_startNode = np.subtract(startNode.getCoordinates(), (nodeSize/2, nodeSize/2))
        center_endNode = np.subtract(endNode.getCoordinates(), (nodeSize/2, nodeSize/2))

        Node_bool = False

        shortestDist = 999999999
        curr_segment = lst.head
        closestNode = curr_segment.data[0]
        while curr_segment:
            dx_end = abs(curr_segment.data[0][0] - endNode.rect.x-10)
            dy_end = abs(curr_segment.data[0][1] - endNode.rect.y-10)
            dx_start = abs(curr_segment.data[0][0] - startNode.rect.x-10)
            dy_start = abs(curr_segment.data[0][1] - startNode.rect.y-10)

            if (distance(curr_segment.data[0], center_startNode) >= distance(curr_segment.data[0], center_endNode)):
                if (dx_end>radius or dy_end>radius):
                    Node_bool = True
                else:
                    Node_bool = False
            elif(distance(curr_segment.data[0], center_startNode) < distance(curr_segment.data[0], center_endNode)):
                if (dx_start>radius or dy_start>radius):
                    Node_bool = True
                else:
                    Node_bool = False

            #distance_from_click = distance(curr_segment.data[0], mouse_pos)
            if(Node_bool):
                #shortestDist = distance_from_click
                closestNode = curr_segment.data[0]
                break
            curr_segment = curr_segment.next
        if(closestNode == lst.head.data[0]):
            print("No point found")
        
        return Node(self.disp.BROWN, nodeSize, nodeSize, closestNode[0], closestNode[1], 2, labelCounter)

    def showControls(self):
        window = Tk()
        window.attributes("-topmost", True)
        window.title("Sprouts Controls")

        def close_window():
            window.destroy()

        #Organise the popup window
        top = Frame(window)
        bottom = Frame(window)
        top.pack(side=TOP)
        bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

        label = Label(window, text="\u2022 Use the left mousebutton to draw a line in freehand \n\n \u2022 Use the right mouse button to do pathfinding \n\n \u2022 After pathfinding, click space to accept the line and esc to delete it \n\n \u2022 Click with the left mouse button to place a new point", background="#ffffff", justify="left")
        button = Button(window, text="OK", command=close_window, bg="white")
        
        label.pack(in_=top)
        button.pack(in_=bottom)
        bottom.configure(bg="white")
        window.mainloop()

    def chooseWinner(self):

        window = Tk()
        window.attributes("-topmost", True)
        window.title("Winner")

        #Organise the popup window
        top = Frame(window)
        bottom = Frame(window)
        top.pack(side=TOP)
        bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

        def continue_game():
            window.destroy()

        # Make new window and widgets for the winner popup
        def end_game():
            def close_end_game():
                root.destroy()

            window.destroy()
            winnerName = ""
            if (displayName == playerOneName): 
                winnerName = playerTwoName
            else:
                winnerName = playerOneName
            root = Tk()
            root.title("Winner")
            label = Label(root, text="The winner of the game is " + winnerName + "! \n\n Congratulations\n", bg="white").pack()
            button = Button(root, text="OK", command=close_end_game, bg="white").pack()
            root.configure(bg="white")
            root.mainloop()
            self.disp.QuitGame()

        # Create widgets
        label = Label(window, text="Can't draw anymore lines? \n\n Press surrender to end game and declare a winner\n", bg="white")
        button1 = Button(window, text="Surrender", command=end_game, bg="white")
        button2 = Button(window, text="Continue Game", command=continue_game, bg="white")

        # Pack widgets into the frames
        label.pack(in_=top)
        button1.pack(in_=bottom, side="left")
        button2.pack(in_=bottom, side="right")

        window.configure(bg="white")
        bottom.configure(bg="white")
        window.mainloop()

    