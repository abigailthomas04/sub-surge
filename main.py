# import pygame library
import pygame
from pygame import * 

# import music
from pygame import mixer

# initialize pygame
pygame.init()

# initalize the music
mixer.init()

# load audio files
bg_music = mixer.music.load('shape-scape/audio/bg_music.mp3')
# game_over_music = mixer.music.load('shape-scape/audio/game_over_audio.mp3')

# set volume
bg_music_volume = mixer.music.set_volume(0.5)
# game_over_music = mixer.music.set_volume(1)

# play the music
bg_music_play = mixer.music.play()
# game_over_music_play = mixer.music.play()

# CONSTANTS
SCREEN_WIDTH = 400     # width of the entire window (x-axis)
SCREEN_HEIGHT = 650    # height of the entire window (y-axis)
SCROLL_SPEED = .15     # speed of the scroll

# variables
scroll = 0             # scroll for the bg
sand_scroll = 0        # scroll for ocean floor to disappear and not repeat
log_scroll = 0         # scroll for logs
subX = 200             # initial x coordinate of submarine
subY = 590             # initial y coordinate of submarine
logX = 200             # intitial x coordinate of log 
logY = 175             # initial y coordinate of log
starting = False       # has player pressed SPACE BAR to start
collision = False      # has player hit obstacle

# draw the screen 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# name the screen
pygame.display.set_caption('ShapeScape')

# upload images
bg = pygame.image.load('shape-scape/img/ocean_bg.png')
sand = pygame.image.load('shape-scape/img/sand.jpg')
seaweed = pygame.image.load('shape-scape/img/seaweed.png')
submarine = pygame.image.load('shape-scape/img/submarine.png')
title = pygame.image.load('shape-scape/img/title.png')
start1 = pygame.image.load('shape-scape/img/press.png')
start2 = pygame.image.load('shape-scape/img/space_bar.png')
start3 = pygame.image.load('shape-scape/img/to_start.png')
end = pygame.image.load('shape-scape/img/game_over_img.png')
log = pygame.image.load('shape-scape/img/log1.png')

# resize images
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
sand = pygame.transform.scale(sand, (SCREEN_WIDTH, 100))
seaweed = pygame.transform.scale(seaweed, (50, 50))
submarine = pygame.transform.scale(submarine, (80, 80))
title = pygame.transform.scale(title, (380, 60))
start1 = pygame.transform.scale(start1, (160, 40))
start2 = pygame.transform.scale(start2, (300, 40))
start3 = pygame.transform.scale(start3, (256, 40))
end = pygame.transform.scale(end, (380, 60))
log = pygame.transform.scale(log, (100, 25))

# hide mouse cursor
pygame.mouse.set_visible(False)

# the ship
class Submarine():

    def __init__(self, x, y):

        self.image = submarine
        self.width = 80
        self.height = 50
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0

    # hopping function, call when player hits UP ARROW
    def hop(self):

        dy = 0
        gravity = .1

        # GRAVITY
        self.vel_y += gravity
        dy += self.vel_y
        self.rect.y += dy

        # stopping player from fallin off bottom of screen
        if self.rect.bottom + dy > SCREEN_HEIGHT - 5:

            dy = 0
            self.vey_y = 0
            self.rect.y = subY
        
        # the to press
        up_arrow = pygame.key.get_pressed()

        # if UP ARROW is pressed, player hops up
        if up_arrow[pygame.K_UP] == True:
            
            # how high player hops after pressing UP ARROW
            self.vel_y = -2.
    
    # draw the submarine in game loop   
    def draw(self):

        screen.blit(self.image, (self.rect.x - 0, self.rect.y - 20))
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

# the obstacles/ logs
class Obstacle():

    def __init__(self, x, y):

        self.image = log
        self.width = 100
        self.height = 25
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

    # draw the obstacles in game loop
    def draw(self):
        
        # to the right
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

# creating instances of classes
sub = Submarine(subX, subY)
log1 = Obstacle(logX - 200, logY)        # log srating on the left of screen to scroll right
log2 = Obstacle(400 + logX, logY + 100)  # log starting on the right of the screen to scroll left

# start menu function
def start_menu():
    
    # draw title and start words
    screen.blit(title, (10, 50))
    screen.blit(start1, (120, 200))
    screen.blit(start2, (54, 300))
    screen.blit(start3, (75, 400))

# make a game_over function
def game_over():    # if collision = True, call this function

    # BG WITH NO SCROLLING
    # draw bg
    screen.blit(bg, (0, 0))
    # draw sand
    screen.blit(sand, (0, 550))

    # draw seaweed
    # left most seaweed
    screen.blit(seaweed, (65, 540))
    # middle seaweed
    screen.blit(seaweed, (235, 530))
    # right most seaweed
    screen.blit(seaweed, (300, 545))


    # draw submarine
    sub.draw()
    sub.rect.y = 590

    # draw game over screen
    screen.blit(end, (10, 200))

run = True
### THE MAIN LOOP ###
while run: 

    # if user clicks exit window, game quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            # break the loop
            run = False

    # check for user to press SPACE BAR
    pressed = pygame.key.get_pressed()
    if (pressed[K_SPACE]) == True:
        starting = True

    # draw background
    screen.blit(bg, (0, scroll))
    screen.blit(bg, (0, scroll - 650))

    # draw sand
    screen.blit(sand, (0, 550 + sand_scroll))

    # draw submarine
    sub.draw()
    
    # if player collides with obstacle
    if sub.rect.colliderect(log1.rect) or sub.rect.colliderect(log2.rect):
        collision = True

    # stop user from going up off screen
    if sub.rect.y < 17:
        sub.rect.y = 17

    # draw seaweed
    # left most seaweed
    screen.blit(seaweed, (65, 540 + sand_scroll))
    # middle seaweed
    screen.blit(seaweed, (235, 530 + sand_scroll))
    # right most seaweed
    screen.blit(seaweed, (300, 545 + sand_scroll))

    # until user presses SPACE BAR, title screen is drawn
    if starting == False:

        # call start menu
        start_menu()

    # game begins after SPACE BAR is pressed, and start menu goes away
    else:
        
        # player hopping
        sub.hop()

        log1.draw()
        log2.draw()

        # scroll the background
        scroll += SCROLL_SPEED
        if abs(scroll) > 650:
            scroll = 0

        # scroll the ocean floor off screen
        sand_scroll += SCROLL_SPEED
        if abs(sand_scroll) > 100:
            sand_scroll = 120

        # to the left
        log1.rect.x += 1
        if log1.rect.x > 500:
            log1.rect.x = -100

        # to the right
        log2.rect.x -= 1
        if log2.rect.x < -100:
            log2.rect.x = 700

    if collision == True:

        # call game over function
        game_over()
        # GOT COLLISION DETECTED 3

    # update the display
    pygame.display.update()

# quit the window
pygame.quit()