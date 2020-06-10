#IMPORTS
import pygame, random
from pygame.locals import *
from squareNode import SquareNode
from linkedList import LinkedList
from point import Point
from intersection import *
import networkx as nx
import numpy as np
from grid import Grid
from itertools import product


#Nodes
 
# Add the node to the list of objects

class SproutsController:
    def __init__(self,pygame,disp):
        self.disp = disp
        self.pygame = pygame
        self.all_sprites_list = pygame.sprite.Group()


    #Allowing the user to close the window...
    def GameLoop(self):

        #FIELDS
        G = Grid(self.disp.size[0],self.disp.size[1])

        LEFT = 1
        RIGHT = 3
        mouse_position = (0, 0)
        pathfinding = False
        drawing = False
        merged = False          #This boolean is checked to make sure that the drawn line was accepted
        last_pos = None
        drawPointsOnce = True
        isInsideNode = True     #Won't draw lines while this is true
        exitedNode = False      #Ignores clicking inside a node to increase it's degree
        nodesHitCounter = 0     #Check whether a line went into more than 2 nodes, if so, then it should be deleted

        #LinkedList
        permLst = LinkedList()
        tempLst = LinkedList()

        #This will be a list that will contain all the sprites we intend to use in our game.
        all_sprites_list = pygame.sprite.Group()

        carryOn = True
        clock=pygame.time.Clock()
 
        while carryOn:
            #https://stackoverflow.com/questions/50503609/how-to-draw-a-continuous-line-in-pygame
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        carryOn=False
                    elif event.type == MOUSEBUTTONDOWN and event.button == RIGHT:
                        #When right mb is pressed, checks if mouse is over a node, if so save node for pathfinding.
                        pos = pygame.mouse.get_pos()
                        for sprite in self.all_sprites_list:
                            if sprite.rect.collidepoint(pos):
                                if (sprite.isFull()):
                                    print("Illegal move, node is full")
                                elif pathfinding:
                                    print("TO")
                                    print(pos)
                                    print("FINDING PATH...")
                                    
                                    
                                    Grid.find_path(last_pos,pos,tempLst,G) #Find path from prev. node to current node.
                                    tempLst.drawLst(self.disp.screen, self.disp.PURPLE)

                                    pathfinding = False
                                    tempNode = None

                                    #remove underlying grid around new edge
                                    Grid.block_nodes(tempLst,G)

                                    #Accept new edge, TODO: add condition for accepting
                                    permLst.merge(tempLst)
                                    merged = True
                                else:
                                    #save pressed node

                                    #debug
                                    print("FROM")
                                    last_pos = pos
                                    print(last_pos)

                                    tempNode = sprite
                                    pathfinding = True #start pathfinding on next click
                                    
                         
                    elif event.type == MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                        if (drawing):
                            pos = pygame.mouse.get_pos()
                            for sprite in self.all_sprites_list:
                                if sprite.rect.collidepoint(pos):
                                    print("Du er stadig inde i node, idiot!")
                                    isInsideNode = True
                                    break
                                else:
                                    isInsideNode = False
                                    exitedNode = True
                            # Add the new line to the linked list and draw the line
                            if last_pos is not None and not isInsideNode:
                                    # Draws a line between the current mouse position and the mouse position from the last frame
                                    tempLst.prepend((last_pos, pos))
                                    tempLst.drawHead(self.disp.screen, self.disp.BLACK)
                            last_pos = pos
                    elif event.type == MOUSEBUTTONUP and event.button == LEFT:
                        #When mouse is released, checks if mouse is over a node
                        pos = pygame.mouse.get_pos()
                        for sprite in self.all_sprites_list:
                            if sprite.rect.collidepoint(pos):
                                if (sprite.isFull() or (sprite == tempNode and sprite.getCounter() >= 2)):
                                    print("Illegal move, node is full")
                                elif (collision(tempLst, permLst)):
                                    print("Der er fandme fucking kollision")
                                elif exitedNode:
                                    #TO:DO add check for whether or not counters are full
                                
                                    #Add edge to perm list of edges.
                                    Grid.block_nodes(tempLst,G)

                                    permLst.merge(tempLst)
                                    merged = True

                                    #increment number of attached lines to both nodes
                                    sprite.incrementCounter()
                                    tempNode.incrementCounter()

                                    print(sprite.getCounter())
                        # Delete drawn line if it didn't end in a sprite
                        if (not merged):
                            # TODO: This can erase existing lines, maybe we should fix
                            tempLst.drawLst(self.disp.screen, self.disp.GREEN)
                        #Reset mouse position, tempList and drawing status on release.
                        mouse_position = (0, 0)
                        last_pos = None
                        drawing = False
                        merged = False
                        exitedNode = False
                        print(tempLst)
                        tempLst = LinkedList()
                    elif event.type == MOUSEBUTTONDOWN and event.button == LEFT:
                        #When mouse is pressed, checks if mouse is over a node, if so start drawing.
                        pos = pygame.mouse.get_pos()
                        for sprite in self.all_sprites_list:
                            if sprite.rect.collidepoint(pos):
                                if (sprite.isFull()):
                                    print("Illegal move, node is full")
                                else:
                                    #save pressed node
                                    tempNode = sprite
                                    drawing = True
                                    exitedNode = False        
                
                #Game Logic
                self.all_sprites_list.update()
        
                #Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
                if (drawPointsOnce):
                    self.all_sprites_list.draw(self.disp.screen)
                    drawPointsOnce = False
                
                permLst.drawLst(self.disp.screen, self.disp.BLACK)

                self.disp.updateScreen(pygame)
              
                #Number of frames per secong e.g. 60
                clock.tick(120)

        pygame.quit()

    def initializeGameState(self, filename,spriteList):
        margin = 100
        y = 1
        x = 1
        firstRead = False
        f = open(filename,"r")
        lines = f.readlines()
        for line in lines:
            if not(firstRead):
                n = int(line)
                for i in range(1,n+1):
                    spriteList.add(SquareNode(self.disp.RED, 20, 20, (margin*x),(margin*y), 0, i))
                    x+=1
                    if ((margin*x)) >= (self.disp.size[0]):
                        x = 1
                        y += 1
                firstRead = True
                print("Done med placering")
                #init edges between nodes as specificed, and check legality
            