import pygame

class SproutsDisplay:
    # Different colors used in the game
    GREEN = (0,200,0)
    LIME_GREEN = (0, 179, 0)
    LIGHT_GREEN =  (20, 255, 140)
    GREY = (210, 210 ,210)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (180, 0, 0)
    LIGHT_RED = (255, 100, 100)
    PURPLE = (255, 0, 255)
    BROWN = (128, 64, 0)

    def __init__(self, screenwidth, screenheight,pygame):
        # Initialize a display
        size = (screenwidth, screenheight)
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Sprouts")

    def updateScreen(self,pygame):
        pygame.display.flip()

    # Redrawn the screen as white, with a simple text and an image
    def loadingScreen(self):
        self.screen.fill(self.WHITE)
        background = pygame.image.load("small_plant.png")
        self.screen.blit(background, (self.size[0]-328, self.size[1]-256+10))
        largeText = pygame.font.Font("Pacifico.ttf", 50) # Choose font and font size
        TextSurf, TextRect = SproutsDisplay.text_objects("Loading...", largeText, self.BLACK) # Get the text surface and the size of the text
        TextRect.center = ((self.size[0]/2, self.size[1]/8)) # Set the center of the text
        self.screen.blit(TextSurf, TextRect)
        pygame.display.update()

    # Render the text and return the rendered text aswell as the rect (how much the text fills)
    def text_objects(text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    # Draw an instruction at the bottom of the screen, telling the player what to do
    def turnInstructions(self, message):
        smallText = pygame.font.Font("freesansbold.ttf", 15)
        TextSurf, TextRect = SproutsDisplay.text_objects(message, smallText, self.BLACK)
        TextRect.center = ((self.size[0]/2, 475))
        pygame.draw.rect(self.screen, self.WHITE, (0, 455, self.size[0], 50))
        self.screen.blit(TextSurf, TextRect)

    # Create a button used in the menu
    def menuButton(self, msg, pos_x, pos_y, width, height, i_color, a_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        #Hightlight button, when mouse hover
        if pos_x+width > mouse[0] > pos_x and pos_y+height > mouse[1] > pos_y:
            pygame.draw.rect(self.screen, a_color, (pos_x, pos_y, width, height), 3)

            if click[0] == 1 and action != None:
                action()
        else: 
            pygame.draw.rect(self.screen, i_color, (pos_x, pos_y, width, height), 3)

        # Set the text on the button and draw the button itself
        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = SproutsDisplay.text_objects(msg, smallText, self.BLACK)
        textRect.center = ((pos_x+(width/2)), (pos_y+(height/2)))
        pygame.draw.rect(self.screen, self.WHITE, (pos_x+3, pos_y+3, width-6, height-6))
        self.screen.blit(textSurf, textRect)

    # Create button used ingame (Has no border)
    def gameButton(self, msg, pos_x, pos_y, width, height, i_color, a_color, isDrawing, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        smallText = pygame.font.Font("freesansbold.ttf", 20)

        #Hightlight text, when mouse hover
        if pos_x+width > mouse[0] > pos_x and pos_y+height > mouse[1] > pos_y:
            textSurf, textRect = SproutsDisplay.text_objects(msg, smallText, a_color)

            if click[0] == 1 and action != None and not isDrawing:
                action()
        else: 
            textSurf, textRect = SproutsDisplay.text_objects(msg, smallText, i_color)

        # Set text and position
        textRect.center = ((pos_x+(width/2)), (pos_y+(height/2)))
        pygame.draw.rect(self.screen, self.WHITE, (pos_x+3, pos_y+3, width-6, height-6))
        self.screen.blit(textSurf, textRect)

    # Write who's players turn it is at the center and top of the screen
    def turnTracker(self, displayName):
        largeText = pygame.font.Font("Pacifico.ttf", 30)
        TextSurf, TextRect = SproutsDisplay.text_objects(displayName, largeText, self.BLACK)
        TextRect.center = ((self.size[0]/2, 20))
        pygame.draw.rect(self.screen, self.WHITE, (self.size[0]/2-60, 0, 120, 50))
        self.screen.blit(TextSurf, TextRect)

    # Menu loop with interactive buttons
    def game_intro(self, controller):
        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.QuitGame()
            
            #Ready the menu screen with text and image
            self.screen.fill(self.WHITE)
            background = pygame.image.load("small_plant.png")
            self.screen.blit(background, (self.size[0]-328, self.size[1]-256+10))
            largeText = pygame.font.Font("Pacifico.ttf", 50)
            TextSurf, TextRect = SproutsDisplay.text_objects("Sprouts", largeText, self.BLACK)
            TextRect.center = ((self.size[0]/2, self.size[1]/8))
            self.screen.blit(TextSurf, TextRect)

            # Create the menu buttons and update the screen
            self.menuButton("START", 200/3, self.size[1]/4+25, 100, 50, self.GREEN, self.LIGHT_GREEN, controller.GameLoop)
            self.menuButton("QUIT", self.size[0]-200/3-100, self.size[1]/4+25, 100, 50, self.RED, self.LIGHT_RED, self.QuitGame)
            pygame.display.update()

    def QuitGame(self):
        pygame.quit()
        quit()