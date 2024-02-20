#Goose Reproduce (Wormy)
#By Iris Jang(IJ), Valeriya Medvedeva(VM), Rose Shi(RS), Nidhi Sarkar(NS)

import random, pygame, sys
from pygame.locals import *

#soundtrack used throughout the game IJ
pygame.init()
bing_sound = pygame.mixer.Sound("137523215.mp3")  
crash_sound = pygame.mixer.Sound("mixkit-dramatic-metal-explosion-impact-1687.wav")

from pygame import mixer
pygame.mixer.init()
#background music IJ
mixer.music.load("Fluffing a duck music.mp3")
mixer.music.play(-1)

#original speed VM
FPS_0 = 8
#variable that counts the number of eggs eaten by the geese VM
N_EGG = 0 
#the background size is set to 600x600 to fit the size of the bakcground picture
WINDOWWIDTH =600
WINDOWHEIGHT = 600
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#setting the different colours using red, green and blue NS
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK
 
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

# add images and speed variables to the main
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, FPS, GOOSE_IMG, EGG_IMG, DUCK_IMG
    #add the images and the corfile names RS
    GOOSE_IMG = pygame.image.load("goose.png")
    EGG_IMG = pygame.image.load("egg.png")
    DUCK_IMG = pygame.image.load("duck.png")
    #set changeable speed FPS to equal to original speed VM
    FPS = FPS_0
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Goose Reproduce')
    
    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()
    

def runGame():
    global N_EGG, FPS, DISPLAYSURF
    #background picture during the game VM
    bgpicture = pygame.image.load("grass.jpg").convert()
    #displays the image as the background VM
    DISPLAYSURF.blit(bgpicture, (0,0))
   
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            #pause the background music when worm hits the wall IJ
            pygame.mixer.music.pause()
           
            return # game over
            
            
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                #pause the background music when the worm hits itself IJ
                pygame.mixer.music.pause()
                return # game over
                

        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            #play bing sound everytime worm eats apple IJ
            pygame.mixer.Sound.play(bing_sound)
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
            #every time a new egg appears on the screen, the N_EGG variable increases by 1 VM
            N_EGG = N_EGG + 1
            #if N_EGG equals to a multiple of 3 the speed (FPS) increases by 3 VM
            if N_EGG%3 == 0:
                FPS = FPS + 3
        else:
            del wormCoords[-1] # remove worm's tail segment
            #unpause background music IJ
            pygame.mixer.music.unpause()

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        #displays the background image VM
        DISPLAYSURF.blit(bgpicture, (0,0))
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    # creates two titles of different colours NS
    # both in font "Free sans bold", size 60 NS
    titleFont = pygame.font.Font('freesansbold.ttf', 60)
    titleSurf1 = titleFont.render('Goose Reproduce', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Goose Reproduce', True, GREEN)
    
    
    degrees1 = 0
    degrees2 = 0
    while True:
        #fills background with shade 'BGCOLOUR' (established in the beginning) NS
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    global N_EGG, FPS, FPS_0
    #sets N_EGG equal to 0 once the game restarts VM
    N_EGG = 0
    #sets changeable variable FPS equal to the orginial speed once the game restarts VM
    FPS = FPS_0
    
    #play crush sound everytime game ends(worm crushes) IJ
    pygame.mixer.Sound.play(crash_sound)
    # displays 'GAME OVER' when player loses in white, Free sans Bold font NS
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)
    
    #fills background with shade 'BGCOLOUR' (established in the beginning) NS
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    # displays player's score in white NS
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        #changes the rectangle with an image of a goose with displaysurf.blit RS
        DISPLAYSURF.blit(GOOSE_IMG,wormSegmentRect)
        #changes the last unit of the worm into a baby duckling RS
    for newHead in wormCoords:
        DISPLAYSURF.blit(DUCK_IMG,wormSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    #changes the rectangle apple into an image of an egg by using the displaysuf.blit function RS
    DISPLAYSURF.blit(EGG_IMG,appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()