import pygame, random
from sproutsDisplay import SproutsDisplay
from sproutsController import SproutsController
from pygame.locals import *
pygame.init()

disp = SproutsDisplay(400,500,pygame)
controller = SproutsController(pygame,disp)
controller.initializeGameState("initialize.txt",controller.all_sprites_list)
controller.GameLoop()