import pygame

class SproutsDisplay:
    GREEN = (20, 255, 140)
    LIME_GREEN = (0, 179, 0)
    LIGHT_GREEN =  (0,200,0)
    GREY = (210, 210 ,210)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    LIGHT_RED = (180, 0, 0)
    PURPLE = (255, 0, 255)
    BROWN = (128, 64, 0)

    def __init__(self, screenwidth, screenheight,pygame):
        size = (screenwidth, screenheight)
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Sprouts")


    def updateScreen(self,pygame):
        pygame.display.flip()
