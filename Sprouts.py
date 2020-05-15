#IMPORTS
import pygame, random
from pygame.locals import *
from squareNode import SquareNode
from grid import Grid
from linkedList import LinkedList

pygame.init()
 
#DEFINE COLORS
GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

#FIELDS
SCREENWIDTH=400
SCREENHEIGHT=500
mouse_position = (0, 0)
drawing = False
merged = False
last_pos = None
size = (SCREENWIDTH, SCREENHEIGHT)

#LinkedList
permLst = LinkedList()
permLst.prepend((1,1))
permLst.prepend((99,99))
tempLst = LinkedList()

#PYGAME INITS
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sprouts")
 
#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
screen.fill(GREEN) 
all_sprites_list.add(SquareNode(RED, 20, 20,100,400))
all_sprites_list.add(SquareNode(RED, 20, 20,200,300))
 
# Add the node to the list of objects
 
#Allowing the user to close the window...
carryOn = True
clock=pygame.time.Clock()
 
while carryOn:
    #https://stackoverflow.com/questions/50503609/how-to-draw-a-continuous-line-in-pygame
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                carryOn=False
            elif event.type == MOUSEMOTION:
                if (drawing):
                    mouse_position = pygame.mouse.get_pos()
                    # Add the new line to the linked list and draw the line
                    if last_pos is not None:
                        # Draws a line between the current mouse position and the mouse position from the last frame
                        tempLst.prepend((last_pos,mouse_position))
                        tempLst.drawHead(screen, BLACK)
                    last_pos = mouse_position
            elif event.type == MOUSEBUTTONUP:
                #When mouse is released, checks if mouse is over a node
                pos = pygame.mouse.get_pos()
                for sprite in all_sprites_list:
                    if sprite.rect.collidepoint(pos):
                        permLst.merge(tempLst)
                        merged = True
                # Delete drawn line if it didn't end in a sprite
                if (not merged):
                    tempLst.drawLst(screen, GREEN)
                mouse_position = (0, 0)
                last_pos = None
                drawing = False
                merged = False
                tempLst = LinkedList()
                print(permLst)
            elif event.type == MOUSEBUTTONDOWN:
                #When mouse is pressed, checks if mouse is over a node, if so start drawing.
                pos = pygame.mouse.get_pos()
                for sprite in all_sprites_list:
                    if sprite.rect.collidepoint(pos): 
                        drawing = True

        #Can draw rectangles on mouse click, TODO: when clicking a rectangle - draw a line to another rectangle.        
                
        #Game Logic
        all_sprites_list.update()
 
        #Drawing on Screen

        
        #Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
        all_sprites_list.draw(screen)
 
        #Refresh Screen
        pygame.display.flip()
 
        #Number of frames per secong e.g. 60
        clock.tick(60)

pygame.quit()