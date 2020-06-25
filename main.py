import pygame, random
from sproutsDisplay import SproutsDisplay
from sproutsController import SproutsController
from pygame.locals import *
pygame.init()

def main(): #Main driver code
    gameIcon = pygame.image.load('images\plant.png')
    pygame.display.set_icon(gameIcon)
    disp = SproutsDisplay(400,500, pygame)
    controller = SproutsController(pygame, disp)
    disp.loadingScreen()
    controller.initializeGameState("initialize.txt")
    disp.game_intro(controller)

if __name__ == "__main__":
    main()
