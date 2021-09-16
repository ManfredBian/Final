'''
Manfred
2021-01-25
ICS3U1
Mrs.Bokhari
This program uses the knowledge learned from this semester to create a advanced video game.
Used for inspiration on how to create my own collision function: https://www.geeksforgeeks.org/collision-detection-in-pygame/
Used for my images: Google Images
(I was told by Mrs.Bokarhi I am allowed to use the frame function and the max() function)
'''
from pygame import *
import os
import random

os.environ['SL_VIDEO_WINDOW_POS'] = "%d, %d" % (20, 20)#sets the position of the game to be higher on the screen
init()
#variables used for screen and color
size = width, height = 1000, 700
screen = display.set_mode(size)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (0, 255, 255)

myFont = font.SysFont("Times New Roman", 65)#changes font used and size of font 
#loading all of the images used for the strart screen
startScreenPic = image.load("StartScreenPic.png")
startScreenPic = transform.scale(startScreenPic, (width, height))
startScreenTitle = image.load("StartScreenTitle.png")
#loading image used for info screen
info = image.load("Info.jpg")
#loading and sizing of spaceship
spaceShipSize = (50, 50)
spaceShip = transform.scale(image.load("spaceShip.png"), spaceShipSize)
#loading and sizing of bullets
bulletSize = (3, 6)
bullet = transform.scale(image.load("laserBullet.png"), bulletSize)
#loading and sizing of e-waste
eWasteSize = (70, 70)
eWaste = transform.scale(image.load("e-Waste.png"), eWasteSize)
#loading and sizing of power up
powerSize = (50, 50)
powerIcon = transform.scale(image.load("powerUp.jpg"), powerSize)

px, py = 475, 600#location of spaceship spawn
#creating variables used for movement
KEY_LEFT = False
KEY_RIGHT = False
KEY_UP = False
KEY_DOWN = False
#creating lists used for program
myBullets = []
eWastes = []
powers = []
#game variables to adjust the game if needed
speed = 10
health = 3
possibility = 0.05
#creating location variables used for mouse and start of screen
startscreenX = 0
mx = my = 0
#creating the score variable
score = 0
#creating stage and power frame and frame counter variable
stage = 1
powerFrame = 0
frameCounter = 0
#creates a list of rectangles used for the buttons on the screen making it easier to input each button when needed
rectList = [draw.rect(screen, WHITE, (375, 200, 250, 75)),
            draw.rect(screen, WHITE, (375, 350, 250, 75)),
            draw.rect(screen, WHITE, (375, 500, 250, 75))]

#creating a collide function that detects when two things collide upon each other 
def collide(b, e, bsize, esize):
    return e[0] < b[0] < e[0] + esize[0] and e[1] < b[1] < e[1] + esize[1] \
           or e[0] < b[0] < e[0] + esize[0] and e[1] < b[1] + bsize[1] < e[1] + e[1] \
           or e[0] < b[0] + bsize[0] < e[0] + esize[0] and e[1] < b[1] < e[1] + esize[1] \
           or e[0] < b[0] + bsize[0] < e[0] + esize[0] and e[1] < b[1] + bsize[1] < e[1] + e[1]

#creating the start screen
def StartScreen(screen, startscreenX):
    screen.blit(startScreenPic, Rect(startscreenX, 0, width, height))#blits start screen picture
    screen.blit(startScreenPic, Rect(startscreenX + width, 0, width, height))#used to create a moving background
    screen.blit(startScreenTitle, Rect(45, 0, 0, 0))#blits title of game
    #used to create a larger rectangle frame over the hovered option
    for rect in rectList:
        draw.rect(screen, WHITE, rect) #draws the rectangles used for the options
        if rect.collidepoint(mx, my):#if your mouse movement collides over the button
            draw.rect(screen, WHITE, rect, 5)#draws a larger frame around the rectangle to make it look like it popped out
    #used to write the options ontop of each of the buttons
    text = myFont.render("Start", True, BLACK)
    screen.blit(text, (435, 200))

    text = myFont.render("Help", True, BLACK)
    screen.blit(text, (435, 350))

    text = myFont.render("Quit", True, BLACK)
    screen.blit(text, (435, 500))

#resets the game making it replayable with restarting the program
def resetGame():
    global myBullets, eWastes, px, py, powers#globalizes all of the variables and lists that require a reset
    #empties the lists, clears the scores, and reset the starting cordinates of the player
    myBullets = []
    eWastes = []
    powers = []
    px, py = 475, 600
    score = 0

#starts game
def StartGame(screen):
    global stage, powerFrame, score#globalizes required variables
    #blits the main screen used
    screen.blit(startScreenPic, Rect(startscreenX, 0, width, height))
    screen.blit(startScreenPic, Rect(startscreenX + width, 0, width, height))
    screen.blit(spaceShip, Rect(px, py, spaceShipSize[0], spaceShipSize[1]))#blits the spaceship (the main player)
    for mbullet in myBullets:#creates bullets
        screen.blit(bullet, Rect(mbullet[0], mbullet[1], bulletSize[0], bulletSize[1]))#blits bullets
        mbullet[1] -= 30#moves bullets up
        #if the bullet goes under 0 removes that bullet
        if mbullet[1] < 0:
            myBullets.remove(mbullet)
        #detection of weather an e-waste is being collided by a bullet
        for e in eWastes:
            if collide(mbullet, e, bulletSize, eWasteSize):#
                e[2] -= 1#if it is removes 1 hp
    #creates e-waste
    for e in eWastes:
        screen.blit(eWaste, Rect(e[0], e[1], eWasteSize[0], eWasteSize[1]))#blits e-waste
        e[1] += 2#adds 2 to the y cordinate of the e-waste
        if e[1] > 700:#if e-wastes goes past y 700
            stage = 3#switches to stage 3 (the end screen)
            resetGame()#resets the game
            break#breaks this code
        if e[2] < 0:#if health of e-waste is under 0
            score += 1#adds one score
            eWastes.remove(e)#removes that e-waste
            if random.random() < possibility:#has a chance given that the random number given between 0 and 1 is less than 0.05
                powers.append([random.randint(0, 1000 - eWasteSize[0]), random.randint(-200, -eWasteSize[1]), health])#appends a powerup into the powerup list with random cordinates
    #used for powerup
    for power in powers:
        screen.blit(powerIcon, Rect(power[0], power[1], powerSize[0], powerSize[1]))#blits the powerup
        power[1] += 2#adds 2 to y corindate of the power
        if power[1] > 700:#if power's y corindate is under 700 
            powers.remove(power)#removes the power

        if collide(power, [px, py], powerSize, spaceShipSize):#if the powerup collides with the spaceship
            powers.remove(power)#power is removed
            powerFrame = 180 #sets the power frame to 180

#used end game screen
def endGame(screen):
    global stage#globalizes stage
    #blits background
    screen.blit(startScreenPic, Rect(startscreenX, 0, width, height))
    screen.blit(startScreenPic, Rect(startscreenX + width, 0, width, height))

    text = myFont.render("SCORE: " + " " * (7 - len(str(score))) + str(score), True, WHITE)#sets text as the word score: and then the score
    screen.blit(text, (275, 200))#blits text
    
    draw.rect(screen, WHITE, rectList[1])#draws middle button
    if rectList[1].collidepoint(mx, my):#if mouse hover collides with the button
        draw.rect(screen, WHITE, rectList[1], 5)#draws a larger rectangle around the button
    #draws the text "Back" over the button
    text = myFont.render("Back", True, BLACK)
    screen.blit(text, (435, 350))

#used for info page
def infoPage(screen):
    global stage#globalizes stage
    #draws the background
    screen.blit(startScreenPic, Rect(startscreenX, 0, width, height))
    screen.blit(startScreenPic, Rect(startscreenX + width, 0, width, height))
    
    screen.blit(info, (185, 50, 500, 500))#blits the info screen
    draw.rect(screen, WHITE, rectList[2])#draws the middle button
    if rectList[2].collidepoint(mx, my):#if mouse hovers over the button
        draw.rect(screen, WHITE, rectList[2], 5)#draws a frame aroudn the rectangle
    #draws the "Back" text over the button
    text = myFont.render("Back", True, BLACK)
    screen.blit(text, (435, 500))
    
#generates the e-wastes
def generateEWaste(n):
    for i in range(n):
        #appends random cordinates to the list of e-wastes also adding health to them
        eWastes.append([random.randint(0, 1000 - eWasteSize[0]), random.randint(-200, -eWasteSize[1]), health])

#variables used to create the main game loop
running = True
myClock = time.Clock()

while running:
    for e in event.get():#gets the event happening
        if e.type == QUIT:#if the event is quitting the game
            running = False#running is false
        if e.type == MOUSEBUTTONDOWN:#if the mouse button is down
            mx, my = e.pos#gets the positions
            if stage == 1 and rectList[0].collidepoint(mx, my):#if stage equals 1 and the start button collides with the mouse down
                generateEWaste(4)#generates first e-wastes
                stage = 2#switches to the game stage

            elif stage == 1 and rectList[2].collidepoint(mx, my):#if stage equals 1 and the quit button is collided with the mouse down
                running = False#running is false

            elif stage == 1 and rectList[1].collidepoint(mx, my):#if stage is 1 and the info button collides with mouse down
                stage = 4#changes stage to show the info page

            elif stage == 3 and rectList[1].collidepoint(mx, my):#if stage is 3 and back button collides with the mouse down
                stage = 1#goes back to stage 1 aka the starting screen

            elif stage == 4 and rectList[2].collidepoint(mx, my):#if stage is 4 and button collides with mouse down
                stage = 1#goes back to stage 1 aka the starting screen
        
        if e.type == MOUSEMOTION:#if event type is mouse motion
            mx, my = e.pos#gets the cordinates and makes it mx and my
        
        if e.type == KEYDOWN:#if key is down
            if e.key == K_LEFT:#if key is left
                KEY_LEFT = True#key_left is equal to true
            if e.key == K_RIGHT:#if key is right
                KEY_RIGHT = True#key_right is equal to true
            if e.key == K_UP:#if key is up
                KEY_UP = True#key_up is equal to true
            if e.key == K_DOWN:#if key is down
                KEY_DOWN = True#key_down is true

        if e.type == KEYUP:#is key is up
            if e.key == K_LEFT:#if key is left
                KEY_LEFT = False#key_left is equal to false
            if e.key == K_RIGHT:#if key is right
                KEY_RIGHT = False#key_right is equal to false
            if e.key == K_UP:#if key is up
                KEY_UP = False#key_up is equal to false
            if e.key == K_DOWN:#if key is down
                KEY_DOWN = False#key_down is true
    #if stage is 1
    if stage == 1:
        #create starting screen and start changing the startscreenx to move the background
        StartScreen(screen, startscreenX)
        startscreenX -= 1
        if startscreenX < -1 * width:
            startscreenX = 0
    #if stage is 2
    elif stage == 2:
        StartGame(screen)#starts the game
        if KEY_LEFT and px >= 0:#if key is left and px isnt biger than 0
            px -= speed#px is subtracted by speed (10)
        if KEY_RIGHT and px <= 950:#if key is right and px isnt bigger than 950
            px += speed#px is adding by speed (10)
        if KEY_UP and py >= 0:#is key is up and py isnt bigger than 0
            py -= speed#py is subtracted by speed
        if KEY_DOWN and py <= 650:#is key is down and py isnt smaller than 650
            py += speed#py is added by speed

        if powerFrame == 0:#if power frame = 0
            if frameCounter % 10 == 0:#if frame counter is devisible by 10
                myBullets.append([px + spaceShipSize[0] / 2, py])#appends a bullet
        else:#or else
            if frameCounter % 5 == 0:#if frame counter is devisible by 5(meaning 2x bullets)
                myBullets.append([px + spaceShipSize[0] / 2, py])#appends bullet

        if frameCounter % 20 == 0:#if frame counter is devisible by 20
            generateEWaste(1)#generates e-waste

    elif stage == 3:#if stage is on 3
        endGame(screen)#shows end game screen

    elif stage == 4:#if stage is on 4
        infoPage(screen)#show info page

    myClock.tick(60)#clock tick is at 60
    display.flip()#displays everything

    frameCounter += 1#adds 1 to frame counter
    if frameCounter == 60:#is frame counter is equal to 60
        frameCounter = 0#resets the frame counter
    #power frame is equal to the largest number between 0 and the powerframe minus 1
    powerFrame = max(0, powerFrame - 1)

quit()
