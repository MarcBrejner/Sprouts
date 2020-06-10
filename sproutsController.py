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

labelCounter = 0
nodeSize = 20

class SproutsController:
    def __init__(self,pygame,disp):
        self.disp = disp
        self.pygame = pygame
        self.all_sprites_list = pygame.sprite.Group()


    #Allowing the user to close the window...
    def GameLoop(self):
        global nodeSize
        global labelCounter

        #FIELDS


        mouse_position = (0, 0)
        drawing = False
        merged = False          #This boolean is checked to make sure that the drawn line was accepted
        last_pos = None
        drawPointsOnce = True
        isInsideNode = True     #Won't draw lines while this is true
        exitedNode = False      #Ignores clicking inside a node to increase it's degree
        placeNewPoint = False

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
                    elif event.type == MOUSEMOTION:
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
                    elif event.type == MOUSEBUTTONUP:
                        #When mouse is released, checks if mouse is over a node
                        pos = pygame.mouse.get_pos()
                        for sprite in self.all_sprites_list:
                            if sprite.rect.collidepoint(pos):
                                if (sprite.isFull() or (sprite == beginningNode and sprite.getCounter() >= 2)):
                                    print("Illegal move, node is full")
                                elif (collision(tempLst, permLst)):
                                    print("Der er fandme fucking kollision")
                                elif (disconnected(tempLst)):
                                    print("Du må ikke tegne over andre punkter... Peanut brain")
                                elif exitedNode:
                                    #TO:DO add check for whether or not counters are full
                                
                                    #Add edge to perm list of edges.

                                    permLst.merge(tempLst)
                                    merged = True

                                    endNode = sprite

                                    #increment number of attached lines to both nodes
                                    sprite.incrementCounter()
                                    beginningNode.incrementCounter()

                                    print(sprite.getCounter())
                                    placeNewPoint = True
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
                    elif event.type == MOUSEBUTTONDOWN:
                        #When mouse is pressed, checks if mouse is over a node, if so start drawing.
                        pos = pygame.mouse.get_pos()
                        if (placeNewPoint):
                            print("Nu skal der sgu laves punkter fyr")
                            position_of_new_sprite = closest_point(pos, tempLst, beginningNode, endNode, nodeSize)
                            self.all_sprites_list.add(SquareNode(self.disp.RED, nodeSize, nodeSize, position_of_new_sprite[0]-nodeSize/2, position_of_new_sprite[1]-nodeSize/2, 2, labelCounter))
                            labelCounter += 1
                            placeNewPoint = False
                            tempLst = LinkedList()
                        else:
                            for sprite in self.all_sprites_list:
                                if sprite.rect.collidepoint(pos):
                                    if (sprite.isFull()):
                                        print("Illegal move, node is full")
                                    else:
                                        #save pressed node
                                        beginningNode = sprite
                                        drawing = True
                                        exitedNode = False
                                        placeNewPoint = False
                
                #Game Logic
                self.all_sprites_list.update()

                permLst.drawLst(self.disp.screen, self.disp.BLACK)
        
                #Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
                #if (drawPointsOnce):
                self.all_sprites_list.draw(self.disp.screen)
                    #drawPointsOnce = False 

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
                for labelCounter in range(1,n+1):
                    spriteList.add(SquareNode(self.disp.RED, nodeSize, nodeSize, (margin*x),(margin*y), 0, labelCounter))
                    x+=1
                    if ((margin*x)) >= (self.disp.size[0]):
                        x = 1
                        y += 1
                firstRead = True
                print("Done med placering")
                #init edges between nodes as specificed, and check legality
    
            