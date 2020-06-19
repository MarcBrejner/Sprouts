import pygame

class SproutsDisplay:
    GREEN = (0,200,0)
    LIME_GREEN = (0, 179, 0)
    LIGHT_GREEN =  (20, 255, 140)
    GREY = (210, 210 ,210)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (180, 0, 0)
    LIGHT_RED = (255, 0, 0)
    PURPLE = (255, 0, 255)
    BROWN = (128, 64, 0)

    def __init__(self, screenwidth, screenheight,pygame):
        size = (screenwidth, screenheight)
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Sprouts")

    def updateScreen(self,pygame):
        pygame.display.flip()

    def loadingScreen(self):
        self.screen.fill(self.WHITE)
        background = pygame.image.load("small_plant.png")
        self.screen.blit(background, (self.size[0]-328, self.size[1]-256+10))
        largeText = pygame.font.Font("Pacifico.ttf", 50)
        TextSurf, TextRect = SproutsDisplay.text_objects("Loading...", largeText)
        TextRect.center = ((self.size[0]/2, self.size[1]/8))
        self.screen.blit(TextSurf, TextRect)
        pygame.display.update()

    def text_objects(text, font):
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()