#IMPORTS
import pygame, random
from pygame.locals import *
from squareNode import SquareNode
from grid import Grid

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
last_pos = None
size = (SCREENWIDTH, SCREENHEIGHT)

#GridTest
gameGrid = Grid(SCREENWIDTH,SCREENHEIGHT,0)
gameGrid.set(200,300,123)
print(gameGrid.get(200,300))


#PYGAME INITS
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Car Racing")
 
#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
screen.fill(GREEN) 
all_sprites_list.add(SquareNode(PURPLE, 20, 30,100,400))
all_sprites_list.add(SquareNode(RED, 20, 30,200,300))
 
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
                    if last_pos is not None:
                        pygame.draw.line(screen, BLACK, last_pos, mouse_position, 1)
                        #TODO: Add lines to gameGrid
                    last_pos = mouse_position
            elif event.type == MOUSEBUTTONUP:
                mouse_position = (0, 0)
                last_pos = None
                drawing = False
            elif event.type == MOUSEBUTTONDOWN:
                drawing = True

            #elif event.type == pygame.MOUSEBUTTONDOWN:
                #mouseX, mouseY = pygame.mouse.get_pos()
                #all_sprites_list.add(SquareNode(RED, 20, 30,mouseX,mouseY))
        
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