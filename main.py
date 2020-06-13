import pygame, random
from sproutsDisplay import SproutsDisplay
from sproutsController import SproutsController
from pygame.locals import *
import pygame_menu
pygame.init()

def main():
    gameIcon = pygame.image.load('plant.png')
    pygame.display.set_icon(gameIcon)
    disp = SproutsDisplay(400,500,pygame)
    controller = SproutsController(pygame,disp)
    controller.initializeGameState("initialize.txt",controller.all_sprites_list)
    controller.game_intro()

if __name__ == "__main__":
    main()
