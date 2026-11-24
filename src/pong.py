import pygame 
import math #imports math for cos and sin (see line 60 and 61)
from random import randint # For randomizing the ball direction
import time # to blink the ball (see ball.blink function)
import pygame_gui as ui # To draw UI


pygame.init()
windowH = 600
windowW = 800
screen = pygame.display.set_mode((windowW, windowH))

# load sounds
bounce_1 = pygame.mixer.Sound("sound_effect/Rebound 1.wav")
bounce_2 = pygame.mixer.Sound("sound_effect/Rebound 2.wav")
Game_start = pygame.mixer.Sound("sound_effect/Game start.wav")
Game_over = pygame.mixer.Sound("sound_effect/Game over.wav")


ColorForBatsAndCircle = (255, 255, 255) # This it the color for most stuff in pong

# UI manager
UImanager = ui.UIManager((windowW, windowH))
run = False # Makes the game run

# All of the bool statements inside the pong game, they scattered everywhere
SendBall = False
DrawBall = True
UI = True
menu = True
Settings = False
run_window = True
TrianglePlay = True
ShouldDrawExit = False
PlayerWon = False
ShouldSendBall = True 
ShouldPlayGameOver = False
CanWin = True
# Player 1 and 2 score
Player1Score = 0
Player2Score = 0

# Max FPS
FPS = 60
WinningScore = 5 # winning socre
# Fonts for texts (you can see the license and ttf file in the pong_font folder)
pong_font = pygame.font.Font("pong_font/PressStart2P-Regular.ttf", 16)
TitleFont = pygame.font.Font("pong_font/PressStart2P-Regular.ttf", 32)

# Size for the win message to make it aligned in the center
TextWidthForWinMessage, TextHeightForWinMessage = TitleFont.size("Player 1 wins!")

# Bat class
class bat(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 1

    def draw(self): # Draws a rectangle for a singular bat
        pygame.draw.rect(screen, ColorForBatsAndCircle, (self.x, self.y, self.w, self.h))

class ball(object): # Ball class
    def __init__(self, radius, x, y, outline_size):
        self.x = x
        self.y = y
        self.radius = radius
        self.direction = 250
        self.speed = 1
        self.outline_size = outline_size
        self.AdaptiveSpeed = False
        self.AdaptiveSpeedIncrAmout = 0.5
        self.AdaptiveSpeedIncrAmountOV = 0

    def draw(self): # Draws the bat and it's black outline (The black outline is to see it clear when it next to the bar)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius + self.outline_size)
        pygame.draw.circle(screen, ColorForBatsAndCircle, (self.x, self.y), self.radius)

    def send(self): # Makes the ball direction angle into a x and y velocity
        vel_x = math.cos(math.radians(self.direction)) * self.speed
        vel_y = math.sin(math.radians(self.direction)) * self.speed
        SendArray = [vel_x, vel_y]
        return SendArray

    def reflect(self): # reflects over the x axis
        self.direction = (360 - self.direction) % 360

    def ReflectHorizon(self): # reflects over the y axis (I know horizon is wrong, I'm too lazy to fix it)
        self.direction = (180 - self.direction) % 360
        if self.AdaptiveSpeed: # Checks if the adaptive speed is on and makes it go up
            self.AdaptiveSpeedIncrAmountOV += self.AdaptiveSpeedIncrAmout

    def blink(self): # Makes the ball blink twice
        for i in range(2): 
            self.draw()
            Bat1.draw()
            Bat2.draw()
            Bar.draw()
            Score1.draw("Score: " + str(Player1Score))
            Score2.draw("Score: " + str(Player2Score))
            CmdHelper.draw("esc to exit")
            pygame.display.flip()
            time.sleep(0.5)
            screen.fill((0,0,0))

            Bat1.draw()
            Bat2.draw()
            Bar.draw()
            Score1.draw("Score: " + str(Player1Score))
            Score2.draw("Score: " + str(Player2Score))
            CmdHelper.draw("esc to exit")
            pygame.display.flip()
            time.sleep(0.5)


def RestartRound(): # Puts every object in the right place to start a new round
    ball.x = windowW / 2 - 12
    ball.y = windowH / 2
    Bat1.x, Bat1.y = windowW // 16, windowH / 2
    Bat2.x, Bat2.y = windowW - windowW // 16, windowH / 2
    ball.direction = randint(0, 360)
    ball.speed -= ball.AdaptiveSpeedIncrAmountOV
    ball.AdaptiveSpeedIncrAmountOV = 0
    ball.send()
    SendBall = True
class Bar(object): # bar class, it's very simple with a constructor and a draw function
    def __init__(self, x, y, w, h):
        self.h = h
        self.w = w
        self.x = x
        self.y = y
    def draw(self): # Draws the bar
        pygame.draw.rect(screen, ColorForBatsAndCircle, (self.x, self.y, self.w, self.h))


class Text(): # Text class
    def __init__ (self, x, y, font):
        self.x = x
        self.y = y
        self.font = font
        self.font = font
    def draw(self, text): # Makes a surface and a rect to blit it on the screen
        Score_surface = self.font.render(text, False, ColorForBatsAndCircle)
        Rect = Score_surface.get_rect(topleft=(self.x, self.y))
        screen.blit(Score_surface, Rect)


class Triangle(object): # Triangle class (The triangle next to the play and settings)
        def __init__(self, vertices, scalar, rotate):
            self.vertices = vertices
            self.scalar = scalar
            self.rotate = rotate
            self.TrianglePlay = True

        def ApplyScalarCoords(self, x, y): # Applies the scalar, scalar and rotation so I don't have to recreate the vertices
            rad = math.radians(self.rotate)
            cos_a = math.cos(rad)
            sin_a = math.sin(rad)
            points = []
            for vx, vy in self.vertices:
                # rotate
                rx = vx * cos_a - vy * sin_a
                ry = vx * sin_a + vy * cos_a
                # scale, then translate
                points.append((rx * self.scalar + x, ry * self.scalar + y))
            return points
        def draw(self, new_x, new_y): # Draws the triangle
            pygame.draw.polygon(screen, ColorForBatsAndCircle, self.ApplyScalarCoords(new_x, new_y))


def TextBoxMaker(x, y, w, h, PlaceHolderNumber): # Makes a inputable box where you can put text
    TextBox = ui.elements.UITextEntryLine(relative_rect=pygame.Rect((x, y), (w, h)), manager=UImanager, placeholder_text=str(PlaceHolderNumber))
    return TextBox

def ButtonMaker(x, y, w, h, PlaceHolderText): # Makes a button
    Button = ui.elements.UIButton(relative_rect=pygame.Rect((x, y), (w, h)), text=PlaceHolderText, manager=UImanager)
    return Button

class HollowRect(object): # Makes a rectangle 
    def __init__(self, x, y, w, h, TextX, TextY, font):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.TextX = TextX
        self.TextY = TextY
        self.font = font
        self.OnYes = False
        self.YesW, self.YesH = font.size("yes")
        self.NoW, self.NoH = font.size("no")

    def drawText(self, text):
        Score_surface = self.font.render(text, False, ColorForBatsAndCircle)
        Rect = Score_surface.get_rect(topleft=(self.TextX, self.TextY))
        screen.blit(Score_surface, Rect)

        if self.OnYes: # Draws the text like the text.draw function but changes the color if the rectangle is on yes or no (Makes the yes black if OnYes and white of not OnYes)
            pygame.draw.rect(screen, ColorForBatsAndCircle, (self.TextX + 20, self.TextY + 40, self.YesW, self.YesH))
            Score_surface = self.font.render("yes", False, (0, 0, 0))
            Rect = Score_surface.get_rect(topleft=(self.TextX + 20, self.TextY + 40))
            screen.blit(Score_surface, Rect)

            Score_surface = self.font.render("no", False, ColorForBatsAndCircle)
            Rect = Score_surface.get_rect(topleft=(self.TextX + 100, self.TextY + 40))
            screen.blit(Score_surface, Rect)
        else:
            pygame.draw.rect(screen, ColorForBatsAndCircle, (self.TextX + 95, self.TextY + 37, self.NoW + 5, self.NoH + 5))
            Score_surface = self.font.render("no", False, (0, 0, 0))
            Rect = Score_surface.get_rect(topleft=(self.TextX + 100, self.TextY + 40))
            screen.blit(Score_surface, Rect)

            Score_surface = self.font.render("yes", False, ColorForBatsAndCircle)
            Rect = Score_surface.get_rect(topleft=(self.TextX + 20, self.TextY + 40))
            screen.blit(Score_surface, Rect)

    def draw(self): # Draws everything minus the yes and no
        pygame.draw.rect(screen, ColorForBatsAndCircle, (self.x - 3, self.y - 3, self.w + 6, self.h + 6))
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.w, self.h))
        self.drawText("Exit game?")

def DrawBakedGame(Ballx, Bally, Bat1y, Bat2y): # Draws the frozen-in-time game in the start menu
    ball.x, ball.y = Ballx, Bally
    Bat1.y, Bat2.y =  Bat1y, Bat2y
    Bat1.draw()
    Bat2.draw()
    ball.draw()

def StartGame(): # Puts everything in the right place to start the gmae
    ball.x, ball.y = windowW / 2 - 12.8, windowH / 2
    Bat1.x, Bat1.y = windowW // 16, windowH / 2
    Bat2.x, Bat2.y = windowW - windowW // 16, windowH / 2 
    Player1Score, Player2Score = 0, 0
    Game_start.play()

# Makes the score classes
Score1 = Text(windowW // 6, windowH // 24, pong_font)
Score2 = Text(windowW - windowW // 3, windowH // 24, pong_font)

# Makes the bar
Bar = Bar(windowW // 2 - 15, 5, 5, windowH)


# Makes the ball and bat
ball = ball(5, windowW / 2 - 12.8, windowH / 2, 1)
Bat1 = bat(windowW // 16, windowH / 2, 5, 50)
Bat2 = bat(windowW - windowW // 16, windowH / 2, 5, 50)

# Makes the play and settings buttons
PlayButton = Text(windowW / 2 - 40, windowH // 2 - 40, pong_font)
SettingsButton = Text(windowW / 2 - 65, windowH // 2 + 10, pong_font)

# Makes the triangle on the left and right of the home screen
TriangleLeft = Triangle([(-1, 0), (1, -1), (1, 1)], 10, 180)
TriangleRight = Triangle([(-1, 0), (1, -1), (1, 1)], 10, 0)


# Tells the players which keys too press
CmdHelper = Text(0, windowH - windowH // 16, pong_font)

# Makes the text box where you can customize the speed of the ball
BallSpeedBox = TextBoxMaker(windowW - windowW // 16 - 50, windowH // 16, 50, 40, ball.speed)
BallSpeedBox.hide()

# Makes the text that indicates that the ball speed box is the ball speed box
BallSpeedTextIndi = Text(windowW // 16, windowH // 16 + 20, pong_font)

# Makes the text box where you can customize the speed of the bat
BatSpeedBox = TextBoxMaker(windowW - windowW // 16 - 50, windowH // 16 + 50, 50, 40, Bat1.speed)
BatSpeedBox.hide()


# Indicates the players that this is the bat speed box
BatSpeedBoxIndi = Text(windowW // 16, windowH // 16 + 70, pong_font)

# Makes the button where you can turn adaptive ball speed on or off
AdaptiveBallSpeedButton = ButtonMaker(windowW - windowW // 16 - 50, windowH // 16 + 100, 50, 40, "off")

# Indicates that is the adaptive ball speed button
AdaptiveBallSpeedButtonIndi = Text(windowW // 16, windowH // 16 + 120, pong_font)

# Makes the title in the home screen
Title = Text(windowW // 2 - 67, windowH // 8, TitleFont)

# Makes the winner message
WinnerMessage = Text(windowW // 2 - TextWidthForWinMessage // 2, windowH // 2 - TextHeightForWinMessage // 2, TitleFont)

# Makes the exit game screen
ExitGameScreen = HollowRect(windowW // 2 - 100, windowH // 2 - 100, 200, 100, windowW // 2 - 84, windowH // 2 - 80, pong_font)

clock = pygame.time.Clock()

while run_window:
    time_delta = clock.tick(FPS) / 1000
    k = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_window = False # quits the window
        if event.type == ui.UI_TEXT_ENTRY_FINISHED and Settings:

            # Checks if the player customized the ball speed and if they did change it
            if event.ui_element == BallSpeedBox:
                ball.speed = float(event.text)

            # Checks if the player customized the bat speed and if they did change it
            elif event.ui_element == BatSpeedBox:
                Bat1.speed = float(event.text)
                Bat2.speed = float(event.text)

        # Checks if the adaptive ball speed button was pressed and turned it on or off
        if event.type == ui.UI_BUTTON_PRESSED:
            if event.ui_element == AdaptiveBallSpeedButton:
                ball.AdaptiveSpeed = not ball.AdaptiveSpeed
        
        # Checks if the player used the up adn down keys to toggle between settings and play
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN) and UI and menu:
                TrianglePlay = not TrianglePlay

            # Checks if the player used left and right to toggle between yes and no in the exit screen
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT) and run and ShouldDrawExit:
                ExitGameScreen.OnYes = not ExitGameScreen.OnYes

            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                # Checks if the player pressed play to start the game
                if UI and menu:                
                    if TrianglePlay:
                        UI, run = False, True
                        ShouldSendBall = True
                        StartGame()
                    # Checks if the player opened the settings menu
                    else: 
                        menu, Settings = False, True
                        
                elif run and ShouldDrawExit:     
                    # Checks if the player put the rectangle on the yes key and if so, exits the game if not just continues the game
                    if ExitGameScreen.OnYes:
                        UI, run = True, False
                        SendBall = False
                        ExitGameScreen.OnYes = False
                    ShouldDrawExit = False

            if event.key == pygame.K_ESCAPE:
                # Checks if the player wants to exit mid-game
                if run and not PlayerWon:
                    ShouldDrawExit = not ShouldDrawExit

                # Checks if the player won and if so just goes into the main menu
                elif run and PlayerWon:
                    UI, run = True, False
                elif Settings:
                    Settings, menu = False, True
                
        # Makes the UI manager process the events
        UImanager.process_events(event)
    # fills the screen black
    screen.fill((0, 0, 0))
    if UI:
        if menu:
            # Draws the buttons
            PlayButton.draw("Play")
            SettingsButton.draw("Settings")

            # Draws the space or enter to select
            CmdHelper.draw("Space or enter to select")

            # Draws the triangles next to the play or settings button
            if TrianglePlay == True:
                TriangleLeft.draw(windowW / 2 - 60, windowH // 2 - 33)
                TriangleRight.draw(windowW / 2 + 44, windowH // 2 - 33)
            else:
                TriangleLeft.draw(windowW / 2 - 85, windowH // 2 + 17)
                TriangleRight.draw(windowW / 2 + 79, windowH // 2 + 17)

            # Draws the pong title
            Title.draw("PONG")

            # Draws the baked game in the background
            DrawBakedGame(400, 200, 100, 500)
        if Settings:
            # Showns the text boxes to input the bat and ball speed
            BallSpeedBox.show()
            BatSpeedBox.show()

            # Draws the text on the adaptive ball speed button 
            if ball.AdaptiveSpeed:
                AdaptiveBallSpeedButton.set_text("on")
            else:
                AdaptiveBallSpeedButton.set_text("off")
            
            # rebuilds the ball speed button
            AdaptiveBallSpeedButton.rebuild()

            # Shows the adaptive ball speed button
            AdaptiveBallSpeedButton.show()
            # Draws the indicators
            BallSpeedTextIndi.draw("Ball speed: ")
            BatSpeedBoxIndi.draw("Bat speed: ")
            AdaptiveBallSpeedButtonIndi.draw("Adaptive ball speed: ")

            # updates the UI manager and draws it
            UImanager.update(time_delta)
            UImanager.draw_ui(screen)

            # Draws the escape indicator
            CmdHelper.draw("esc to exit")

            # Checks if the escape key has been pressed
            if k[pygame.K_ESCAPE]:
                Settings, menu = False, True
            

  
        
    if run:
        # Checks if the game should play (the exit screen blocks this)
        if SendBall and not ShouldDrawExit:

            # Makes the ball go in a direction if it's in the window boundaries
            if ball.y + ball.radius < windowH and ball.y - ball.radius > 0 and ball.x + ball.radius < windowW and ball.x - ball.radius > 0:
                Send_array = ball.send()
                ball.x += Send_array[0]
                ball.y += Send_array[1]

            # Bounces the ball and sends it on it's way
            elif ball.y + ball.radius > windowH or ball.y - ball.radius < 0: 
                bounce_1.play()
                ball.reflect()
                Send_array = ball.send()
                ball.x += Send_array[0]
                ball.y += Send_array[1] 

            # Checks if the ball has hit the sides of teh screen
            else:
                SendBall = False
                ball.blink()
                ShouldSendBall = True
                if ball.x < windowW / 2:
                    Player2Score += 1
                    RestartRound()
                else: 
                    Player1Score += 1
                    RestartRound()
            
            # Makes the rectangle for collisions
            ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius * 2, ball.radius * 2)
            bat1_rect = pygame.Rect(Bat1.x, Bat1.y, Bat1.w, Bat1.h)
            bat2_rect = pygame.Rect(Bat2.x, Bat2.y, Bat2.w, Bat2.h)
            
            # Checks if the ball and bat1 or 2 are overlapping and if so reflects them
            if ball_rect.colliderect(bat1_rect) and Send_array[0] < 0:
                ball.ReflectHorizon()
                bounce_2.play()

            elif ball_rect.colliderect(bat2_rect) and Send_array[0] > 0:
                ball.ReflectHorizon()
                bounce_2.play() 

        # Checks for key presses
        if not ShouldDrawExit:
            if k[pygame.K_w] and Bat1.y - 5 > 0:
                Bat1.y -= 5 * Bat1.speed
            if k[pygame.K_s] and Bat1.y + Bat1.h + 5 < windowH:
                Bat1.y += 5 * Bat1.speed
            if k[pygame.K_UP] and Bat2.y - 5 > 0:
                Bat2.y -= 5 * Bat2.speed
            if k[pygame.K_DOWN] and Bat2.y +  Bat2.h + 5 < windowH:
                Bat2.y += 5 * Bat2.speed
            if k[pygame.K_b]:
                SendBall = True
                ShouldSendBall = False

        # Checks if one of the players won
        if Player1Score == WinningScore:
            WinnerMessage.draw("Player 1 wins!")
            if CanWin:
                PlayerWon = True
                ShouldPlayGameOver = True
        if Player2Score == WinningScore:
            WinnerMessage.draw("Player 2 wins!")
            if CanWin:
                PlayerWon = True
                ShouldPlayGameOver = True
        
        # Draws everything
        Bat1.draw()
        Bat2.draw()
        Bar.draw()
        ball.draw()
        Score1.draw("Score: " + str(Player1Score))
        Score2.draw("Score: " + str(Player2Score))

        # Checks if the ball is sent or not to draw ether "esc to exit and b to start round" or just "esc to exit"
        if ShouldSendBall:
            CmdHelper.draw("esc to exit b to start round")
        else:
            CmdHelper.draw("esc to exit")
        if ShouldDrawExit:
            ExitGameScreen.draw()
        if ShouldPlayGameOver and CanWin:
            Game_over.play()
            CanWin = False
    pygame.display.flip()

    # Quits pygame
pygame.quit()
