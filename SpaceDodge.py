## Achievements:

# 90 seconds on easy: "One and a Half"
# 60 seconds on normal: "Hang on a minute"
# 45 seconds on hard: "You're hard"
# 30 seconds on diabolical: "Did you see that?"
# Fill the score board: "Been there done that"
# Die in less than 1 seconds: "I can't even"
# View the credits 5 times: "Aww you care about me"

# Credits:
# Tommy, Harley, Zoe, Gemma

# Highscore
# Include names
# left and right arrows to navigate through difficulties

# Display highscores on death screens


import pygame
import time
import random
import math
from enum import Enum

pygame.init()
clock = pygame.time.Clock()

display_width = 500
display_height = 500
space_between_buttons = (display_width+display_height)/200
game_display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Space dodge')

# Create colours
black  = (0,0,0)
white  = (255,255,255)
red    = (255,0,0)
green  = (0,255,0)
blue   = (0,0,255)
cyan   = (0,255,255)
yellow = (255,255,0)

# Create common message position
title = (display_width*(10/20),display_height*(4/20))

# Load up players and details about players
player_image = [pygame.image.load('star.png'), pygame.image.load('star2.png')]
player_width = 11
player_height = 11
player_speed = 2

# load up game icon
icon = pygame.image.load('starlogo.png')
pygame.display.set_icon(icon)

def LoadScores():
    score_data=[ [], [], [], [] ]
    try:
        scoresheet = open("scoresheet.txt", 'r')
    except:
        scoresheet = open("scoresheet.txt", 'w')
        score_string = '0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n'
        scoresheet.write(score_string)
        scoresheet.close()
        scoresheet = open("scoresheet.txt", 'r')
    for mode in Difficulty:
        for n in range(0,5):
            line = scoresheet.readline()
            score_data[mode.value].append(float(line.strip()))
    scoresheet.close()
    return score_data
class Difficulty(Enum):
    Easy = 0
    Normal = 1
    Hard = 2
    Diabolical = 3
def SaveScores(score_data):
    scoresheet = open("scoresheet.txt", 'w')
    score_string = ''
    for mode in Difficulty:
        for n in range(0,5):
            score_string += str(score_data[mode.value][n])+'\n'
    scoresheet.write(score_string)
def RecordScores(score, number):
    new_highscore = False
    n = int(number/4-1)
    modes = [Difficulty.Easy.value, Difficulty.Normal.value, Difficulty.Hard.value, '', Difficulty.Diabolical.value]
    score_data[modes[n]].append(score)
    score_digits = len(score)-1
    score_data[modes[n]].sort(key = float)
    score_data[modes[n]].pop(0)
    if score_data[modes[n]][-2] == float(score):
        new_highscore = True
    return score_data, new_highscore

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
    elif direction == 'down':
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

def InitialiseButtons():
    buttons = {'Main Menu'  :{'x'     : display_width    *(10/20),
                              'y'     : display_height   *(13/20)+4*space_between_buttons,
                              'width' : display_width    *(12/20),
                              'height': display_height   *(2 /20),
                              'action': MainMenu               } ,
               'Play'       :{'x'     : display_width    *(10/20),
                              'y'     : display_height   *(9 /20),
                              'width' : display_width    *(12/20),
                              'height': display_height   *(2 /20)} ,
               'Highscores' :{'x'     : display_width    *(7/20)-space_between_buttons/2,
                              'y'     : display_height   *(11/20)+2*space_between_buttons,
                              'width' : display_width    *(6/20)-space_between_buttons,
                              'height': display_width    *(2/20)} ,
               'Credits'    :{'x'     : display_width    *(13/20)+space_between_buttons/2,
                              'y'     : display_height   *(11/20)+2*space_between_buttons,
                              'width' : display_width    *(6/20)-space_between_buttons,
                              'height': display_width    *(2/20)} ,
               'Easy'       :{'x'     : display_width    *(7/20)-space_between_buttons/2,
                              'y'     : display_height   *(9/20),
                              'width' : display_width    *(6/20)-space_between_buttons,
                              'height': display_width    *(2/20),
                              'numof_things': 4 } ,
               'Normal'     :{'x'     : display_width    *(13/20)+space_between_buttons/2,
                              'y'     : display_height   *(9/20),
                              'width' : display_width    *(6/20)-space_between_buttons,
                              'height': display_width    *(2/20),
                              'numof_things': 8 } ,
               'Hard'       :{'x'     : display_width   *(7/20)-space_between_buttons/2,
                              'y'     : display_height   *(11/20)+2*space_between_buttons,
                              'width' : display_width  *(6/20)-space_between_buttons,
                              'height': display_width     *(2/20),
                              'numof_things': 12 } ,
               'Diabolical' :{'x'     : display_width  *(13/20)+space_between_buttons/2,
                              'y'     : display_height   *(11/20)+2*space_between_buttons,
                              'width' : display_width  *(6/20)-space_between_buttons,
                              'height': display_width     *(2/20),
                              'numof_things': 20 } ,
              'Instructions':{'x'     : display_width    *(7/20)-space_between_buttons/2,
                              'y'     : display_height   *(13/20)+4*space_between_buttons,
                              'width' : display_width    *(6/20)-space_between_buttons,
                              'height': display_height   *(2 /20)} ,
              'Multiplayer'  :{'x'     : display_width    *(13/20)+space_between_buttons/2,
                              'y'     : display_height   *(13/20)+4*space_between_buttons,
                              'width' : display_width    *(6/20)-space_between_buttons,
                              'height': display_height   *(2 /20)} }
    return buttons

def CreateButton(x , y, width, height, colour = red, hover_colour = white, text = 'hello', text_colour = black):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width/2 > mouse[0] > x - width/2 and y + height/2 > mouse[1] > y - height/2:
        pygame.draw.rect(game_display, hover_colour, (x-width/2,y-height/2,width,height))
        if click[0] == 1:
            time.sleep(0.2)
            # If the button has been clicked, return True so that when the function is called it can activate whatever action needs to be activated with whatever variables it needs!
            return(True)
    else:
        pygame.draw.rect(game_display, colour, (x-width/2,y-height/2,width,height))
    MessageDisplay(text = text, position = (x,y), colour = text_colour)

def MainMenu(intro = True):

    # Initialise background things
    all_things = range(0,20)
    t = InitialiseThings(all_things)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                SaveScores(score_data)
                quit()

        game_display.fill(black)

        # Have Things fly in background
        for thing in all_things:
            t['x'][thing], t['y'][thing], t['delay'][thing] = MoveThing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
            DisplayThing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)

        MessageDisplay(text = 'Space Dodge', position = title, text_size = 50)

        if CreateButton(x = buttons['Play']['x'], y = buttons['Play']['y'], width = buttons['Play']['width'], height = buttons['Play']['height'], text = 'Play'):
            DifficultySelection()
        if CreateButton(x = buttons['Highscores']['x'], y = buttons['Highscores']['y'], width = buttons['Highscores']['width'], height = buttons['Highscores']['height'], text = 'Highscores'):
            Highscores()
        if CreateButton(x = buttons['Credits']['x'], y = buttons['Credits']['y'], width = buttons['Credits']['width'], height = buttons['Credits']['height'], text = 'Credits'):
            Credits()
        if CreateButton(x = buttons['Instructions']['x'], y = buttons['Instructions']['y'], width = buttons['Instructions']['width'], height = buttons['Instructions']['height'], text = 'Instructions'):
            Instructions()
        if CreateButton(x = buttons['Multiplayer']['x'], y = buttons['Multiplayer']['y'], width = buttons['Multiplayer']['width'], height = buttons['Multiplayer']['height'], text = 'Multiplayer'):
            MultiplayerDifficultySelection()


        pygame.display.update()
        clock.tick(60)
    intro = False
def Instructions(instructions = True):

    # Initialise background things
    all_things = range(0,20)
    t = InitialiseThings(all_things)

    while instructions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                SaveScores(score_data)
                quit()

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

        if CreateButton(buttons['Main Menu']['x'], buttons['Main Menu']['y'], buttons['Main Menu']['width'], buttons['Main Menu']['height'], text = 'Main Menu'):
            MainMenu()

        pygame.display.update()
        clock.tick(60)
    instructions = False
def Highscores(highscore = True, difficulty = Difficulty.Normal):

    # Initialise background things
    all_things = range(0,20)
    t = InitialiseThings(all_things)

    while highscore == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                SaveScores(score_data)
                quit()
        game_display.fill(black)

        # Have Things fly in background
        for thing in all_things:
            t['x'][thing], t['y'][thing], t['delay'][thing] = MoveThing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
            DisplayThing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)

        # Black backdrop so things dont obscure display of scores
        pygame.draw.rect(game_display, black, [display_width*(4/20), display_height*(6/20), display_width*(12/20), display_height*(7/20)])

        MessageDisplay(text = 'Highscores', position = title, text_size = 50)
        MessageDisplay(text = difficulty.name, text_size = 20, position = (display_width*(10/20),display_height*(6/20)))

        for number, score in enumerate(score_data[difficulty.value], start = 1):
            MessageDisplay(text = str(score), position = (display_width*((8)/20),display_height*((13-1.1*number)/20)), text_size = 20)

        if CreateButton(x = buttons['Main Menu']['x'], y = buttons['Main Menu']['y'], width = buttons['Main Menu']['width'], height = buttons['Main Menu']['height'], text = 'Main Menu'):
            MainMenu()

        pygame.display.update()
        clock.tick(60)
    highscore == False
def Credits(credits = True):

    # Initialise background things
    all_things = range(0,20)
    t = InitialiseThings(all_things)

    while credits:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                SaveScores(score_data)
                quit()
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

        if CreateButton(x = buttons['Main Menu']['x'], y = buttons['Main Menu']['y'], width = buttons['Main Menu']['width'], height = buttons['Main Menu']['height'], text = 'Main Menu'):
            MainMenu()

        MessageDisplay(text = 'Thank you Tommy, Harley, Zoe and Gemma', position = (display_width/2, display_height*(17/20)), text_size = 20)

        pygame.display.update()
        clock.tick(60)

def DifficultySelection(settings = True):

    # Initialise background things
    all_things = range(0,20)
    t = InitialiseThings(all_things)

    while settings == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                SaveScores(score_data)
                quit()
        game_display.fill(black)

        # Have Things fly in background
        for thing in all_things:
            t['x'][thing], t['y'][thing], t['delay'][thing] = MoveThing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
            DisplayThing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)

        MessageDisplay(text = 'Play', position = title, text_size = 50)
        MessageDisplay(text = 'Choose Difficulty', text_size = 20, position = (display_width*(10/20),display_height*(6.5/20)))

        if CreateButton(x = buttons['Easy']['x'], y = buttons['Easy']['y'], width = buttons['Easy']['width'], height = buttons['Easy']['height'], text = 'Easy'):
            GameLoop(numof_things = buttons['Easy']['numof_things'])
        if CreateButton(x = buttons['Normal']['x'], y = buttons['Normal']['y'], width = buttons['Normal']['width'], height = buttons['Normal']['height'], text = 'Normal'):
            GameLoop(numof_things = buttons['Normal']['numof_things'])
        if CreateButton(x = buttons['Hard']['x'], y = buttons['Hard']['y'], width = buttons['Hard']['width'], height = buttons['Hard']['height'], text = 'Hard'):
            GameLoop(numof_things = buttons['Hard']['numof_things'])
        if CreateButton(x = buttons['Diabolical']['x'], y = buttons['Diabolical']['y'], width = buttons['Diabolical']['width'], height = buttons['Diabolical']['height'], text = 'Diabolical'):
            GameLoop(numof_things = buttons['Diabolical']['numof_things'])

        if CreateButton(x = buttons['Main Menu']['x'], y = buttons['Main Menu']['y'], width = buttons['Main Menu']['width'], height = buttons['Main Menu']['height'], text = 'Main Menu'):
            MainMenu()

        pygame.display.update()
        clock.tick(60)

def MultiplayerDifficultySelection(settings = True):

    # Initialise background things
    all_things = range(0,20)
    t = InitialiseThings(all_things)

    while settings == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                SaveScores(score_data)
                quit()
        game_display.fill(black)

        # Have Things fly in background
        for thing in all_things:
            t['x'][thing], t['y'][thing], t['delay'][thing] = MoveThing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
            DisplayThing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)

        MessageDisplay(text = 'Multiplayer', position = title, text_size = 50)
        MessageDisplay(text = 'Choose Difficulty', text_size = 20, position = (display_width*(10/20),display_height*(6.5/20)))

        if CreateButton(x = buttons['Easy']['x'], y = buttons['Easy']['y'], width = buttons['Easy']['width'], height = buttons['Easy']['height'], text = 'Easy'):
            MultiplayerGameLoop(numof_things = buttons['Easy']['numof_things'])
        if CreateButton(x = buttons['Normal']['x'], y = buttons['Normal']['y'], width = buttons['Normal']['width'], height = buttons['Normal']['height'], text = 'Normal'):
            MultiplayerGameLoop(numof_things = buttons['Normal']['numof_things'])
        if CreateButton(x = buttons['Hard']['x'], y = buttons['Hard']['y'], width = buttons['Hard']['width'], height = buttons['Hard']['height'], text = 'Hard'):
            MultiplayerGameLoop(numof_things = buttons['Hard']['numof_things'])
        if CreateButton(x = buttons['Diabolical']['x'], y = buttons['Diabolical']['y'], width = buttons['Diabolical']['width'], height = buttons['Diabolical']['height'], text = 'Diabolical'):
            MultiplayerGameLoop(numof_things = buttons['Diabolical']['numof_things'])

        if CreateButton(x = buttons['Main Menu']['x'], y = buttons['Main Menu']['y'], width = buttons['Main Menu']['width'], height = buttons['Main Menu']['height'], text = 'Main Menu'):
            MainMenu()

        pygame.display.update()
        clock.tick(60)

def GameLoop(game_start_speed = 100, pause = False, game_over = False, paused_time = 0, numof_things = 8):
    game_speed = game_start_speed
    start_time = time.time()
    exit_game = False

    all_things = range(0,numof_things)
    t = InitialiseThings(all_things)

    player_x = display_width * 0.5
    player_y = display_height * 0.5
    player_x_change = 0
    player_y_change = 0

    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                exit_game == True
            if event.type == pygame.KEYDOWN:

                # Pause the Game
                if event.key == pygame.K_SPACE:
                    if pause == False:
                        pause = True
                        pause_start = time.time()
                    elif pause == True:
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

        if game_over == True:
            score_data, new_highscore = RecordScores(score = str(alive_time), number = numof_things)
            if new_highscore == True:
                Gameover(score_data = score_data, numof_things = numof_things, post_game_message = 'New Highscore...!')
            else:
                Gameover(score_data = score_data, numof_things = numof_things)
        else:
            if pause == False:

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
                    if player_x - t['width'][thing] < t['x'][thing] and t['x'][thing] < player_x + player_width and player_y - t['height'][thing] < t['y'][thing] and t['y'][thing] < player_y + player_height:
                        game_over = True

                alive_time = round(current_time-start_time-paused_time,1)
                clock.tick(game_speed)
                game_speed = game_start_speed + 2*round(current_time-start_time-paused_time)

                MessageDisplay(str(alive_time), text_size = 20, position = ((25),(25)), colour = cyan)
                MessageDisplay(str(game_speed), text_size = 20, position = ((display_width-25),(25)), colour = cyan)
                pygame.display.update()

            elif pause == True:
                MessageDisplay('Paused',50, position = ((display_width/2),(display_height/2)), colour = cyan)
                if CreateButton(x = buttons['Main Menu']['x'], y = buttons['Main Menu']['y'], width = buttons['Main Menu']['width'], height = buttons['Main Menu']['height'], text = 'Main Menu'):
                    MainMenu()
                pygame.display.update()

def MultiplayerGameLoop(game_start_speed = 100, pause = False, game_over = False, paused_time = 0, numof_things = 8, multiplayer_lives = [10,10]):
    game_speed = game_start_speed
    start_time = time.time()
    exit_game = False

    # Possiblity for more than 2 players in future
    numof_players = 2

    all_things = range(0,numof_things)

    t = InitialiseThings(all_things)

    player_x = []
    player_y = []
    player_x_change = []
    player_y_change = []
    for n in range(0,numof_players):
        player_x.append(display_width * 0.5)
        player_y.append(display_height * 0.5)
        player_x_change.append(0)
        player_y_change.append(0)

    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                exit_game == True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if pause == False:
                        pause = True
                        pause_start = time.time()
                    elif pause == True:
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

                if numof_players == 2:
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

                if numof_players == 2:
                    if event.key == pygame.K_a:
                        player_x_change[1] = 0
                    if event.key == pygame.K_d:
                        player_x_change[1] = 0
                    if event.key == pygame.K_w:
                        player_y_change[1] = 0
                    if event.key == pygame.K_s:
                        player_y_change[1] = 0

        else:
            if pause == False:

                current_time = time.time()
                game_display.fill(black)

                for thing in all_things:
                    t['x'][thing], t['y'][thing], t['delay'][thing] = MoveThing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
                    DisplayThing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)

                for n in range(0,numof_players):
                    player_x[n] += player_x_change[n]
                    player_y[n] += player_y_change[n]
                    game_display.blit(player_image[n], (player_x[n],player_y[n]))

                    # Crash into side of screen
                    if player_x[n] > display_width - player_width or player_x[n] < 0 or player_y[n] > display_height - player_height or player_y[n] < 0:
                        game_over = True
                        loser = n
                        multiplayer_lives[n] -= 1
                        MultiplayerGameover(numof_things, loser, multiplayer_lives)
                    #Crash into things
                    for thing in all_things:
                        if player_x[n] - t['width'][thing] < t['x'][thing] and t['x'][thing] < player_x[n] + player_width and player_y[n] - t['height'][thing] < t['y'][thing] and t['y'][thing] < player_y[n] + player_height:
                            game_over = True
                            loser = n
                            multiplayer_lives[n] -= 1
                            MultiplayerGameover(numof_things, loser, multiplayer_lives)

                alive_time = round(current_time-start_time-paused_time,1)
                clock.tick(game_speed)
                game_speed = game_start_speed + 2*round(current_time-start_time-paused_time)

                # Time Alive
                MessageDisplay(str(alive_time), text_size = 20, position = ((display_width/2),(25)), colour = cyan)
                # Game Speed
                MessageDisplay(str(game_speed), text_size = 20, position = ((display_width/2),(50)), colour = cyan)
                # Yellow Score
                MessageDisplay(str(multiplayer_lives[0]), text_size = 20, position = ((25),(25)), colour = yellow)
                # Blue Score
                MessageDisplay(str(multiplayer_lives[1]), text_size = 20, position = ((display_width-25),(25)), colour = cyan)

                pygame.display.update()

                
            elif pause == True:
                MessageDisplay('Paused',50, position = ((display_width/2),(display_height/2)), colour = cyan)
                if CreateButton(x = buttons['Main Menu']['x'], y = buttons['Main Menu']['y'], width = buttons['Main Menu']['width'], height = buttons['Main Menu']['height'], text = 'Main Menu'):
                    MainMenu()
                pygame.display.update()

def Gameover(numof_things, score_data, post_game_message = ''):
    gameover = True
    while gameover:
        MessageDisplay('Game Over', text_size = 50, position = title, colour = cyan)

        if post_game_message != '':
            pygame.draw.rect(game_display, black, (display_width*(6/20),display_height*(5.5/20),display_width*(6.5/20),display_height*(2/20)))
            MessageDisplay(post_game_message, text_size = 20, position = (display_width*(10/20),display_height*(6.5/20)), colour = yellow)

        if CreateButton(display_width/2, display_height*(4.5/10), display_height/2, display_width/10, text = 'Play Again (Enter)'):
            GameLoop(numof_things)

        if CreateButton(display_width/2, display_height*(6/10), display_width/2, display_width/10, text = 'Main Menu'):
            MainMenu()

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    GameLoop(numof_things = numof_things)
            if event.type == pygame.QUIT:
                SaveScores(score_data)
                quit()
                exit_game == True

def MultiplayerGameover(numof_things, loser, multiplayer_lives):

    # If both players still have lives left
    if multiplayer_lives[0]!= 0 and multiplayer_lives[1]!=0:
        pygame.draw.rect(game_display, black, (display_width*(7/20),display_height*(5.5/20),display_width*(6/20),display_height*(2/20)))
        if loser == 0:
            MessageDisplay('Blue Won!', text_size = 20, position = (display_width*(10/20),display_height*(6.5/20)), colour = cyan)
        elif loser == 1:
            MessageDisplay('Yellow Won!', text_size = 20, position = (display_width*(10/20),display_height*(6.5/20)), colour = yellow)
        pygame.display.update()
        time.sleep(1)
        MultiplayerGameLoop(numof_things = numof_things, multiplayer_lives = multiplayer_lives)
    gameover = True

    while gameover:

        MessageDisplay('Game Over', text_size = 50, position = title, colour = cyan)

        if CreateButton(display_width/2, display_height*(4.5/10), display_height/2, display_width/10, text = 'Play Again (Enter)'):
            print("here(button click)")
            MultiplayerGameLoop(numof_things = numof_things, multiplayer_lives = [3,3])

        if CreateButton(display_width/2, display_height*(6/10), display_width/2, display_width/10, text = 'Main Menu'):
            MainMenu()

        # Yellow Score
        MessageDisplay(str(multiplayer_lives[0]), text_size = 20, position = ((25),(25)), colour = yellow)
        # Blue
        MessageDisplay(str(multiplayer_lives[1]), text_size = 20, position = ((display_width-25),(25)), colour = cyan)

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("here")
                    MultiplayerGameLoop(numof_things = numof_things, multiplayer_lives = [3,3])
            if event.type == pygame.QUIT:
                SaveScores(score_data)
                quit()
                exit_game == True


score_data = LoadScores()
buttons = InitialiseButtons()
MainMenu()
