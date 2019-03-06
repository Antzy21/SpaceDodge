# TODO: Achievements:
#  90 seconds on easy: "One and a Half"
#  60 seconds on normal: "Hang on a minute"
#  45 seconds on hard: "You're hard"
#  30 seconds on diabolical: "Did you see that?"
#  Fill the score board: "Been there done that"
#  Die in less than 1 seconds: "I can't even"
#  View the credits 5 times: "Aww you care about me"

# TODO:  Credits:
#  Tommy, Harley, Zoe, Gemma
# TODO: Clean up credits

# TODO: If times are equal, pick old one first

# TODO: Different colour for multiplayer selection (blue)
# TODO: Establish draws for multiplayer
# TODO: Say who won overall after all lives lost
# TODO: Don't start round until both players have moved

# TODO: Clean up button class
# TODO: Clean up TextOnBlock

# TODO: Use data storage module
# TODO: Big overhaul for loading up data
# TODO: Save data when new record is produced

# TODO: Make way of skipping insert highscore name
# TODO: Make milestones for highscores
# TODO: pygame.quit() when on input name section needs sorting

import pygame
import time
import random
import math
from enum import Enum
import re
import pickle

pygame.init()
clock = pygame.time.Clock()

display_width = 500
display_height = 500
space_between_buttons = (display_width+display_height)/200
game_display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Space dodge')

# Create colours
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
yellow = (255, 255, 0)

# Create common message position
title = (display_width*(10/20), display_height*(4/20))

# Load up players and details about players
player_image = [pygame.image.load('star.png'), pygame.image.load('star2.png')]
player_width = 11
player_height = 11
player_speed = 2

# load up game icon
icon = pygame.image.load('starlogo.png')
pygame.display.set_icon(icon)

def LoadScores():
    try:
        pickle_in = open("BinaryScoresheet.pickle","rb")
        load_difficulties = pickle.load(pickle_in)
    except ValueError:
        load_difficulties = Difficulties()
    return load_difficulties
def SaveScores():
    pickle_out = open("BinaryScoresheet.pickle","wb")
    pickle.dump(difficulties, pickle_out)
    pickle_out.close()
def RecordScore(score, name, difficulty):
    difficulty.highscore.append(Highscore(score, name))
    difficulty.highscore.sort(key = lambda scr : scr.score)
    if len(difficulty.highscore)>5:
        difficulty.highscore.pop(0)
def NewHighscore(n,score):
    suffixes = ['st', 'nd', 'rd', 'th', 'th']
    TextOnBlock(NewHighscoreBlock, text = str(n+1)+str(suffixes[n])+' place!'+' : '+str(score), colour = black, text_colour = yellow)
    MessageDisplay(text = 'New Highscore', position = (display_width*(1/2), display_height*(7/20)), colour = yellow)
    MessageDisplay(text = 'Enter Name', position = (display_width*(1/2), display_height*(9/20)), colour = yellow)
    needs_name = True
    input = ''
    while needs_name:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input != '':  # Don't accept no name
                        needs_name = False
                elif event.key == pygame.K_BACKSPACE:
                    input = input[0:-1]
                elif len(input) < 7:
                    if 48 <= event.key <= 57:  # If it's a number
                        input += chr(event.key)
                    elif 97 <= event.key <= 122:  # If it's a letter, make it a capital
                        input += chr(event.key -32)
        TextOnBlock(GOMainMenuButton)
        spacedInput = ''
        for x in input:
            spacedInput += x + ' '
        TextOnBlock(InsertHighScore, text=spacedInput, colour=black, text_colour=red)
        pygame.display.update()
        clock.tick(30)
    RecordScore(score, input, difficulties.i)

def MessageDisplay(text = '"insert text"',text_size = 20, position = (display_width/2,display_height/2), colour = white):
    largeText = pygame.font.Font('freesansbold.ttf',text_size)
    text_surface = largeText.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.center = position
    game_display.blit(text_surface, text_rect)

def DisplayThing(thingx, thingy, thingw, thingh, colour):
    pygame.draw.rect(game_display, colour, [thingx, thingy, thingw, thingh])
def InitialiseThing(direction, height = 10, width = 10, speed = 2):
    if direction == 'right':
        y = random.randrange(0, display_height-height)
        x = -width
    elif direction == 'left':
        y = random.randrange(0, display_height-height)
        x = display_width
    elif direction == 'up':
        x = random.randrange(0, display_width-width)
        y = display_height
    else: # direction == 'down':
        x = random.randrange(0, display_width-width)
        y = -height
    delay = random.randrange(0, (display_width+display_height)/4)
    return x, y, height, width, speed, direction, delay
def InitialiseThings(all_things):
    direction_list = ['up','down','left','right']
    t = {'x':[],'y':[],'height':[],'width':[],'speed':[],'direction':[],'delay':[]}
    for thing in all_things:
        x, y, height, width, speed, direction, delay = InitialiseThing(direction_list[thing % 4])
        t['x'].append(x)
        t['y'].append(y)
        t['height'].append(height)
        t['width'].append(width)
        t['speed'].append(speed)
        t['direction'].append(direction)
        t['delay'].append(delay)
    return t
def MoveThing(direction, x, y, w, h, speed, delay):
    if delay > 0:
        delay += -1
        return x, y, delay
    else:
        if direction == 'right':
            x +=   speed
            if x > display_width:
                x = - w
                y = random.randrange(0,display_height-h)
            return x, y, delay
        elif direction == 'left':
            x += - speed
            if x < - w :
                x = display_width
                y = random.randrange(0,display_height-h)
            return x, y, delay
        elif direction == 'down':
            y += - speed
            if y < - h:
                y = display_height
                x = random.randrange(0,display_width-w)
            return x, y, delay
        elif direction == 'up':
            y += speed
            if y > display_height:
                y = - h
                x = random.randrange(0,display_width-w)
            return x, y, delay

def CreateButton(button, colour = red, hover_colour = white, text = 'hello', text_colour = black):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if button.x + button.width/2 > mouse[0] > button.x - button.width/2 and button.y + button.height/2 > mouse[1] > button.y - button.height/2:
        TextOnBlock(button, colour = hover_colour, text = text, text_colour = text_colour)
        if click[0] == 1:
            time.sleep(0.2)
            # If the button has been clicked, return True so that when the function is called it can activate whatever action needs to be activated with whatever variables it needs!
            return True
    else:
        TextOnBlock(button, colour = colour, text = text, text_colour = text_colour)
    MessageDisplay(text = text, position = (button.x, button.y), colour = text_colour)
def TextOnBlock(coordinates, colour = red, text = '', text_colour = black):
    pygame.draw.rect(game_display, colour, (coordinates.x-coordinates.width/2,coordinates.y-coordinates.height/2,coordinates.width,coordinates.height))
    MessageDisplay(text = text, position = (coordinates.x, coordinates.y), colour = text_colour)

def MainMenu():

    # Initialise background things
    all_things = range(0,20)
    t = InitialiseThings(all_things)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                SaveScores()
                quit()

        game_display.fill(black)

        # Have Things fly in background
        for thing in all_things:
            t['x'][thing], t['y'][thing], t['delay'][thing] = MoveThing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
            DisplayThing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)

        MessageDisplay(text = 'Space Dodge', position = title, text_size = 50)

        if CreateButton(button = PlayButton, text = 'Play'):
            DifficultySelection()
        if CreateButton(button = HighscoreButton, text = 'Highscores'):
            Highscores()
        if CreateButton(button = CreditsButton, text = 'Credits'):
            Credits()
        if CreateButton(button = InstructionsButton, text = 'Instructions'):
            Instructions()
        if CreateButton(button = MultiplayerButton, text = 'Multiplayer'):
            MultiplayerDifficultySelection()


        pygame.display.update()
        clock.tick(60)
def Instructions():

    # Initialise background things
    all_things = range(0,20)
    t = InitialiseThings(all_things)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                SaveScores()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainMenu()

        game_display.fill(black)

        # Have Things fly in background
        for thing in all_things:
            t['x'][thing], t['y'][thing], t['delay'][thing] = MoveThing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
            DisplayThing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)

        # Black backdrop so things dont obscure display of scores
        pygame.draw.rect(game_display, black, [display_width*(4/20), display_height*(6/20), display_width*(12/20), display_height*(7/20)])

        MessageDisplay(text = 'Instructions', position = title, text_size = 50)

        MessageDisplay(text = 'This is you:', position = (display_width*(9/20),display_height*(6/20)), text_size = 20)
        game_display.blit(icon, (display_width*(12/20),display_height*(6/20)-17))

        MessageDisplay(text = 'Avoid these:', position = (display_width*(9/20),display_height*(7.5/20)), text_size = 20)
        pygame.draw.rect(game_display, white, [display_width*(12/20), display_height*(7.5/20)-17, 30, 30])

        MessageDisplay(text = 'Arrow keys to move', position = (display_width/2,display_height*(9/20)), text_size = 20)
        MessageDisplay(text = '(w,a,s,d for second player)', position = (display_width/2,display_height*(10/20)), text_size = 20)
        MessageDisplay(text = 'Space bar to pause', position = (display_width/2,display_height*(11/20)), text_size = 20)
        MessageDisplay(text = 'Enter to play again', position = (display_width/2, display_height*(12/20)), text_size = 20)
        #MessageDisplay(text = 'Harley Taylor while tommy fiddle his diddle ', position = (display_width/2, display_height*(10.5/20)), text_size = 20)

        if CreateButton(button = MainMenuButton, text = 'Main Menu'):
            MainMenu()

        pygame.display.update()
        clock.tick(60)
def Highscores():

    # Initialise background things
    all_things = range(0,20)
    t = InitialiseThings(all_things)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                SaveScores()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainMenu()
                elif event.key == pygame.K_LEFT:
                    if difficulties.i != difficulties.easy:
                        difficulties.prev()
                elif event.key == pygame.K_RIGHT:
                    if difficulties.i !=  difficulties.diabolical:
                        difficulties.next()
        game_display.fill(black)

        # Have Things fly in background
        for thing in all_things:
            t['x'][thing], t['y'][thing], t['delay'][thing] = MoveThing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
            DisplayThing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)

        # Black backdrop so things dont obscure display of scores
        pygame.draw.rect(game_display, black, [display_width*(4/20), display_height*(6/20), display_width*(12/20), display_height*(7/20)])

        MessageDisplay(text = 'Highscores', position = title, text_size = 50)
        MessageDisplay(text = difficulties.i.name, text_size = 20, position = (display_width*(10/20),display_height*(6/20)))

        for n, score in enumerate(reversed(difficulties.i.highscore)):
            MessageDisplay(text = str(score.score), position = (display_width*(8/20),display_height*((8+1.1*n)/20)), text_size = 20)
            MessageDisplay(text = score.scorer, position = (display_width*(11/20),display_height*((8+1.1*n)/20)), text_size = 20)

        if difficulties.i !=  difficulties.easy:
            if CreateButton(button = ScoreLeftButton, text = '<'):
                difficulties.prev()
                Highscores()
        if difficulties.i !=  difficulties.diabolical:
            if CreateButton(button = ScoreRightButton, text = '>'):
                difficulties.next()
                Highscores()

        if CreateButton(button = MainMenuButton, text = 'Main Menu'):
            MainMenu()

        pygame.display.update()
        clock.tick(60)
def Credits():

    # Initialise background things
    all_things = range(0,20)
    t = InitialiseThings(all_things)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                SaveScores()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainMenu()
        game_display.fill(black)

        # Have Things fly in background
        for thing in all_things:
            t['x'][thing], t['y'][thing], t['delay'][thing] = MoveThing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
            DisplayThing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)

        # Black backdrop so things dont obscure display of scores
        pygame.draw.rect(game_display, black, [display_width*(6/20), display_height*(6/20), display_width*(8/20), display_height*(7/20)])

        MessageDisplay(text = 'Credits', position = title, text_size = 50)
        MessageDisplay(text = 'Space Dodge', position = (display_width/2,display_height*(7.5/20)), text_size = 20)
        MessageDisplay(text = 'Created on Python', position = (display_width/2,display_height*(8.5/20)), text_size = 20)
        MessageDisplay(text = 'Anthony Dunford', position = (display_width/2, display_height*(10.5/20)), text_size = 20)
        #MessageDisplay(text = 'Harley Taylor while tommy fiddle his diddle ', position = (display_width/2, display_height*(10.5/20)), text_size = 20)
        MessageDisplay(text = 'December 2017', position = (display_width/2, display_height*(11.5/20)), text_size = 20)

        if CreateButton(button = MainMenuButton, text = 'Main Menu'):
            MainMenu()

        MessageDisplay(text = 'Thank you Tommy, Harley, Zoe and Gemma', position = (display_width/2, display_height*(17/20)), text_size = 20)

        pygame.display.update()
        clock.tick(60)

def DifficultySelection():

    # Initialise background things
    all_things = range(0,20)
    t = InitialiseThings(all_things)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                SaveScores()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainMenu()
                elif event.key == pygame.K_LEFT:
                    if difficulties.i != difficulties.easy:
                        difficulties.prev()
                elif event.key == pygame.K_RIGHT:
                    if difficulties.i !=  difficulties.diabolical:
                        difficulties.next()
                elif event.key == pygame.K_RETURN:
                    GameLoop()
        game_display.fill(black)

        # Have Things fly in background
        for thing in all_things:
            t['x'][thing], t['y'][thing], t['delay'][thing] = MoveThing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
            DisplayThing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)

        MessageDisplay(text = 'Play', position = title, text_size = 50)
        MessageDisplay(text = 'Choose Difficulty', text_size = 20, position = (display_width*(10/20),display_height*(6.5/20)))

        if difficulties.i !=  difficulties.easy:
            if CreateButton(button = ScoreLeftButton, text = '<'):
                difficulties.prev()
        if difficulties.i !=  difficulties.diabolical:
            if CreateButton(button = ScoreRightButton, text = '>'):
                difficulties.next()

        MessageDisplay(text = difficulties.i.name, text_size= 20, position= (display_width*(10/20),display_height*(9/20)))

        if CreateButton(button = MplayButton, text = 'Play'):
            GameLoop()

        if CreateButton(button = MainMenuButton, text = 'Main Menu'):
            MainMenu()

        pygame.display.update()
        clock.tick(60)
def MultiplayerDifficultySelection(settings = True):

    # Initialise background things
    all_things = range(0,20)
    t = InitialiseThings(all_things)
    lives = 3

    while settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                SaveScores()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    MainMenu()
                elif event.key == pygame.K_LEFT:
                    if difficulties.i != difficulties.easy:
                        difficulties.prev()
                elif event.key == pygame.K_RIGHT:
                    if difficulties.i !=  difficulties.diabolical:
                        difficulties.next()
                elif event.key == pygame.K_RETURN:
                    MultiplayerGameLoop(multiplayer_lives = [lives,lives])
        game_display.fill(black)

        # Have Things fly in background
        for thing in all_things:
            t['x'][thing], t['y'][thing], t['delay'][thing] = MoveThing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
            DisplayThing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)

        MessageDisplay(text = 'Multiplayer', position = title, text_size = 50)
        MessageDisplay(text = 'Choose Difficulty', text_size = 20, position = (display_width*(10/20),display_height*(6.5/20)))

        if difficulties.i !=  difficulties.easy:
            if CreateButton(button = ScoreLeftButton, text = '<'):
                difficulties.prev()
        if difficulties.i !=  difficulties.diabolical:
            if CreateButton(button = ScoreRightButton, text = '>'):
                difficulties.next()
        MessageDisplay(text = difficulties.i.name, text_size= 20, position= (display_width*(10/20),display_height*(9/20)))

        if lives != 0:
            if CreateButton(button = LivesLeftButton, text = '<'):
                lives += -1
        if lives != 20:
            if CreateButton(button = LivesRightButton, text = '>'):
                lives += 1
        MessageDisplay(text = 'Lives: '+str(lives), text_size= 20, position= (display_width*(10/20),display_height*(11/20)+2*s))

        if CreateButton(button = MultiplayerButton, text = 'Play'):
            MultiplayerGameLoop(multiplayer_lives = [lives,lives])

        if CreateButton(button = InstructionsButton, text = 'Main Menu'):
            MainMenu()

        pygame.display.update()
        clock.tick(60)
def GameLoop(game_start_speed = 100, pause = False, game_over = False, paused_time = 0):
    game_speed = game_start_speed
    start_time = time.time()
    exit_game = False
    alive_time = 0
    pause_start = 0

    all_things = range(0, difficulties.i.numof_things)
    t = InitialiseThings(all_things)

    player_x = display_width * 0.5
    player_y = display_height * 0.5
    player_x_change = 0
    player_y_change = 0

    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:

                # Pause the Game
                if event.key == pygame.K_SPACE:
                    if not pause:
                        pause = True
                        pause_start = time.time()
                    else:
                        pause = False
                        pause_end = time.time()
                        paused_time += pause_end - pause_start

                if event.key == pygame.K_LEFT:
                    player_x_change = - player_speed
                if event.key == pygame.K_RIGHT:
                    player_x_change =   player_speed
                if event.key == pygame.K_UP:
                    player_y_change = - player_speed
                if event.key == pygame.K_DOWN:
                    player_y_change =   player_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player_x_change= 0
                if event.key == pygame.K_RIGHT:
                    player_x_change = 0
                if event.key == pygame.K_UP:
                    player_y_change = 0
                if event.key == pygame.K_DOWN:
                    player_y_change = 0

        if game_over:
            Gameover(alive_time)
        else:
            if not pause:

                current_time = time.time()
                game_display.fill(black)

                for thing in all_things:
                    t['x'][thing], t['y'][thing], t['delay'][thing] = MoveThing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
                    DisplayThing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)


                player_x += player_x_change
                player_y += player_y_change
                game_display.blit(player_image[0], (player_x,player_y))

                # Crash into side of screen
                if player_x > display_width - player_width or player_x < 0 or player_y > display_height - player_height or player_y < 0:
                    game_over = True
                #Crash into things
                for thing in all_things:
                    if player_x - t['width'][thing] < t['x'][thing] < player_x + player_width and player_y - t['height'][thing] < t['y'][thing] < player_y + player_height:
                        game_over = True

                alive_time = round(current_time-start_time-paused_time,1)
                clock.tick(game_speed)
                game_speed = game_start_speed + 2*round(current_time-start_time-paused_time)

                MessageDisplay(str(alive_time), text_size = 20, position = (25, 25), colour = cyan)
                MessageDisplay(str(game_speed), text_size = 20, position = (display_width-25, 25), colour = cyan)
                pygame.display.update()

            else:
                MessageDisplay('Paused',50, position = ((display_width/2),(display_height/2)), colour = cyan)
                if CreateButton(button = MainMenuButton, text = 'Main Menu'):
                    MainMenu()
                pygame.display.update()
def MultiplayerGameLoop(multiplayer_lives, game_start_speed = 100, pause = False, paused_time = 0):
    game_speed = game_start_speed
    start_time = time.time()
    exit_game = False
    pause_start = 0

    all_things = range(0,difficulties.i.numof_things)

    t = InitialiseThings(all_things)

    player_x = []
    player_y = []
    player_x_change = []
    player_y_change = []
    for n in range(0,2):
        player_x.append(display_width * 0.5)
        player_y.append(display_height * 0.5)
        player_x_change.append(0)
        player_y_change.append(0)

    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not pause:
                        pause = True
                        pause_start = time.time()
                    else:
                        pause = False
                        pause_end = time.time()
                        paused_time += pause_end - pause_start

                if event.key == pygame.K_LEFT:
                    player_x_change[0] = - player_speed
                if event.key == pygame.K_RIGHT:
                    player_x_change[0] =   player_speed
                if event.key == pygame.K_UP:
                    player_y_change[0] = - player_speed
                if event.key == pygame.K_DOWN:
                    player_y_change[0] =   player_speed
                if event.key == pygame.K_a:
                    player_x_change[1] = - player_speed
                if event.key == pygame.K_d:
                    player_x_change[1] =   player_speed
                if event.key == pygame.K_w:
                    player_y_change[1] = - player_speed
                if event.key == pygame.K_s:
                    player_y_change[1] =   player_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player_x_change[0] = 0
                if event.key == pygame.K_RIGHT:
                    player_x_change[0] = 0
                if event.key == pygame.K_UP:
                    player_y_change[0] = 0
                if event.key == pygame.K_DOWN:
                    player_y_change[0] = 0
                if event.key == pygame.K_a:
                    player_x_change[1] = 0
                if event.key == pygame.K_d:
                    player_x_change[1] = 0
                if event.key == pygame.K_w:
                    player_y_change[1] = 0
                if event.key == pygame.K_s:
                    player_y_change[1] = 0

        else:
            if not pause:

                current_time = time.time()
                game_display.fill(black)

                for thing in all_things:
                    t['x'][thing], t['y'][thing], t['delay'][thing] = MoveThing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
                    DisplayThing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)

                for n in range(0,2):
                    player_x[n] += player_x_change[n]
                    player_y[n] += player_y_change[n]
                    game_display.blit(player_image[n], (player_x[n],player_y[n]))

                    # Crash into side of screen
                    if player_x[n] > display_width - player_width or player_x[n] < 0 or player_y[n] > display_height - player_height or player_y[n] < 0:
                        loser = n
                        multiplayer_lives[n] -= 1
                        MultiplayerGameover(loser, multiplayer_lives)
                    #Crash into things
                    for thing in all_things:
                        if player_x[n] - t['width'][thing] < t['x'][thing] < player_x[n] + player_width and player_y[n] - t['height'][thing] < t['y'][thing] < player_y[n] + player_height:
                            loser = n
                            multiplayer_lives[n] -= 1
                            MultiplayerGameover(loser, multiplayer_lives)

                alive_time = round(current_time-start_time-paused_time,1)
                clock.tick(game_speed)
                game_speed = game_start_speed + 2*round(current_time-start_time-paused_time)

                # Time Alive
                MessageDisplay(str(alive_time), text_size = 20, position = ((display_width/2),25), colour = cyan)
                # Game Speed
                MessageDisplay(str(game_speed), text_size = 20, position = ((display_width/2),50), colour = cyan)
                # Yellow Score
                MessageDisplay(str(multiplayer_lives[0]), text_size = 20, position = (25,25), colour = yellow)
                # Blue Score
                MessageDisplay(str(multiplayer_lives[1]), text_size = 20, position = (display_width-25,25), colour = cyan)

                pygame.display.update()

            else:
                MessageDisplay('Paused',50, position = ((display_width/2),(display_height/2)), colour = cyan)
                if CreateButton(button = MainMenuButton, text = 'Main Menu'):
                    MainMenu()
                pygame.display.update()
def Gameover(score):
    gameover = True

    MessageDisplay('Game Over', text_size = 50, position = title, colour = cyan)

    if not difficulties.i.highscore: # if empty list
        NewHighscore(n = 0, score = score)
    else:
        for n, highscore in enumerate(reversed(difficulties.i.highscore)):
            if highscore.score < score:
                NewHighscore(n, score)
                break

    while gameover:

        TextOnBlock(NewHighscoreBlock, black)

        if CreateButton(button = PlayAgainButton, text = 'Play Again (Enter)'):
            GameLoop()

        if CreateButton(button = GOMainMenuButton, text = 'Main Menu (Esc)'):
            MainMenu()

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    GameLoop()
                if event.key == pygame.K_ESCAPE:
                    MainMenu()
            if event.type == pygame.QUIT:
                SaveScores()
                quit()
def MultiplayerGameover(loser, multiplayer_lives):

    # If both players still have lives left
    if multiplayer_lives[0]!= 0 and multiplayer_lives[1]!=0:
        pygame.draw.rect(game_display, black, (display_width*(7/20),display_height*(5.5/20),display_width*(6/20),display_height*(2/20)))
        if loser == 0:
            MessageDisplay('Blue Won!', text_size = 20, position = (display_width*(10/20),display_height*(6.5/20)), colour = cyan)
        elif loser == 1:
            MessageDisplay('Yellow Won!', text_size = 20, position = (display_width*(10/20),display_height*(6.5/20)), colour = yellow)
        pygame.display.update()
        time.sleep(1)
        MultiplayerGameLoop(multiplayer_lives = multiplayer_lives)

    while True:

        MessageDisplay('Game Over', text_size = 50, position = title, colour = cyan)

        if CreateButton(PlayAgainButton, text = 'Play Again (Enter)'):
            MultiplayerGameLoop(multiplayer_lives = [3,3])

        if CreateButton(GOMainMenuButton, text = 'Main Menu (Esc)'):
            MainMenu()

        # Yellow Score
        MessageDisplay(str(multiplayer_lives[0]), text_size = 20, position = (25,25), colour = yellow)
        # Blue
        MessageDisplay(str(multiplayer_lives[1]), text_size = 20, position = (display_width-25, 25), colour = cyan)

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    MultiplayerGameLoop(multiplayer_lives = [3,3])
                if event.key == pygame.K_ESCAPE:
                    MainMenu()
            if event.type == pygame.QUIT:
                SaveScores()
                quit()

class Highscore:
    def __init__(self, score, name):
        self.score = score
        self.scorer = name
class Difficulty:
    def __init__(self, enum, number_of_things, name):
        self.enum = enum
        self.numof_things = number_of_things
        self.name = name
        self.highscore = []
class Difficulties:
    def __iter__(self):
        self.n = 0
        return self
    def __next__(self):
        if self.n == 0:
            self.n = self.easy
        elif self.n == self.easy:
            self.n = self.normal
        elif self.n == self.normal:
            self.n = self.hard
        elif self.n == self.hard:
            self.n = self.diabolical
        else:
            raise StopIteration
        return self.n
    def prev(self):
        if self.i == self.hard:
            self.i = self.normal
        elif self.i == self.normal:
            self.i = self.easy
        elif self.i == self.diabolical:
            self.i = self.hard
        elif self.i == self.easy:
            self.i = self.diabolical
        return self.i
    def next(self):
        if self.i == self.easy:
            self.i = self.normal
        elif self.i == self.normal:
            self.i = self.hard
        elif self.i == self.hard:
            self.i = self.diabolical
        elif self.i == self.diabolical:
            self.i = self.easy
        return self.i
    def __init__(self):
        self.easy = Difficulty(0,4,'Easy')
        self.normal = Difficulty(1,8,'Normal')
        self.hard = Difficulty(2,12,'Hard')
        self.diabolical = Difficulty(3,20,'Diabolical')
        self.i = self.normal

class Button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

s = space_between_buttons
MainMenuButton     = Button(display_width *(10/20),     display_height *(13/20)+4*s, display_width *(12/20),  display_height *(2 /20))
PlayButton         = Button(display_width *(10/20),     display_height *(9 /20),     display_width *(12/20),  display_height *(2 /20))
HighscoreButton    = Button(display_width *(7/20)-s/2,  display_height *(11/20)+2*s, display_width *(6/20)-s, display_height  *(2/20))
ScoreLeftButton    = Button(display_width *(5/20),      display_height *(9/20),      display_width *(2/20),   display_height  *(2/20))
ScoreRightButton   = Button(display_width *(15/20),     display_height *(9/20),      display_width *(2/20),   display_height  *(2/20))
LivesLeftButton    = Button(display_width *(5/20),      display_height *(11/20)+2*s, display_width *(2/20),  display_height  *(2/20))
LivesRightButton   = Button(display_width *(15/20),     display_height *(11/20)+2*s, display_width *(2/20),  display_height  *(2/20))
CreditsButton      = Button(display_width *(13/20)+s/2, display_height *(11/20)+2*s, display_width *(6/20)-s, display_height  *(2/20))
EasyButton         = Button(display_width *(7/20)-s/2,  display_height *(9/20),      display_width *(6/20)-s, display_height  *(2/20))
NormalButton       = Button(display_width *(13/20)+s/2, display_height *(9/20),      display_width *(6/20)-s, display_height  *(2/20))
HardButton         = Button(display_width *(7/20)-s/2,  display_height *(11/20)+2*s, display_width *(6/20)-s, display_height  *(2/20))
DiabolicalButton   = Button(display_width *(13/20)+s/2, display_height *(11/20)+2*s, display_width *(6/20)-s, display_height  *(2/20))
InstructionsButton = Button(display_width *(7/20)-s/2,  display_height *(13/20)+4*s, display_width *(6/20)-s, display_height *(2 /20))
MultiplayerButton  = Button(display_width *(13/20)+s/2, display_height *(13/20)+4*s, display_width *(6/20)-s, display_height *(2 /20))
MplayButton        = Button(display_width *(10/20),     display_height *(11/20)+2*s, display_width *(12/20),  display_height *(2 /20))
GOMainMenuButton   = Button(display_width *(10/20),     display_height *(12/20),     display_width *(10/20),  display_height  *(2/20))
PlayAgainButton    = Button(display_width *(10/20),     display_height*(4.5/10),     display_width *(10/20),   display_height  *(2/20))
InsertHighScore    = Button(display_width *(10/20),     display_height *(12/20),     display_width *(10/20)-2*s,  display_height *(2/20)-2*s)
NewHighscoreBlock  = Button(display_width *(10/20),     display_height*(4/10),       display_width *(10/20),   display_height  *(4/20))

def PrintDifficulties():
    for d in difficulties:
        PrintDifficulty(d)
    print('i: ',vars(difficulties.i))
def PrintDifficulty(difficulty):
    print(vars(difficulty))
    for h in difficulty.highscore:
        print(h.score, h.scorer)

difficulties = LoadScores()
MainMenu()
