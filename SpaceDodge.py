import pygame
import time
import random
import math

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

# Load up "Player 1" and details about "Player 1"
player_image = [pygame.image.load('star.png'), pygame.image.load('star2.png')]
icon = pygame.image.load('starlogo.png')
player_width = 11
player_height = 11
player_speed = 2

# load up game icon
game_icon = pygame.image.load('Starlogo.png')
pygame.display.set_icon(game_icon)

def load_scores():
    score_data={'Easy':[],'Normal':[],'Hard':[],'Diabolical':[]}
    try:
        scoresheet = open("scoresheet.txt", 'r')
    except:
        scoresheet = open("scoresheet.txt", 'w')
        score_string = '0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n0.0\n'
        scoresheet.write(score_string)
        scoresheet.close()
        scoresheet = open("scoresheet.txt", 'r')
    for mode in ['Easy','Normal','Hard','Diabolical']:
        for n in range(0,5):
            line = scoresheet.readline()
            score_data[mode].append(float(line.strip()))
    scoresheet.close()
    return score_data

def save_scores(score_data):
    scoresheet = open("scoresheet.txt", 'w')
    score_string = ''
    for mode in ['Easy','Normal','Hard','Diabolical']:
        for n in range(0,5):
            score_string += str(score_data[mode][n])+'\n'
    scoresheet.write(score_string)

def record_scores(score, number):
    new_highscore = False
    modes = ['Easy','Normal','Hard','','Diabolical']
    n = int(number/4-1)
    score_data[modes[n]].append(score)
    score_digits = len(score)-1
    score_data[modes[n]].sort(key = float)
    score_data[modes[n]].pop(0)
    if score_data[modes[n]][-2] == float(score):
        new_highscore = True
    return score_data, new_highscore

def message_display(text = '"insert text"',text_size = 20, position = (display_width/2,display_height/2), colour = white):
    largeText = pygame.font.Font('freesansbold.ttf',text_size)
    text_surface = largeText.render(text, True, colour)
    text_rect = text_surface.get_rect()
    text_rect.center = position
    game_display.blit(text_surface, text_rect)

def display_thing(thingx, thingy, thingw, thingh, colour):
    pygame.draw.rect(game_display, colour, [thingx, thingy, thingw, thingh])

def initialise_thing(direction, height = 10, width = 10, speed = 2):
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

def initialise_things(all_things,direction_list):
    t = {'x':[],'y':[],'height':[],'width':[],'speed':[],'direction':[],'delay':[]}
    for thing in all_things:
        x, y, height, width, speed, direction, delay = initialise_thing(direction_list[thing % 4])
        t['x'].append(x)
        t['y'].append(y)
        t['height'].append(height)
        t['width'].append(width)
        t['speed'].append(speed)
        t['direction'].append(direction)
        t['delay'].append(delay)
    return t

def move_thing(direction, x, y, w, h, speed, delay):
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

def initialise_buttons():
    buttons = {'Main Menu'  :{'x'     : display_width    *(10/20),
                              'y'     : display_height   *(13/20)+4*space_between_buttons,
                              'width' : display_width    *(12/20),
                              'height': display_height   *(2 /20),
                              'action': intro_loop               } ,
               'Play'       :{'x'     : display_width    *(10/20),
                              'y'     : display_height   *(9 /20),
                              'width' : display_width    *(12/20),
                              'height': display_height   *(2 /20),
                              'action': play_loop                } ,
               'Highscores' :{'x'     : display_width   *(7/20)-space_between_buttons/2,
                              'y'     : display_height   *(11/20)+2*space_between_buttons,
                              'width' : display_width  *(6/20)-space_between_buttons,
                              'height': display_width     *(2/20),
                              'action': highscores_loop          } ,
               'Credits'    :{'x'     : display_width  *(13/20)+space_between_buttons/2,
                              'y'     : display_height   *(11/20)+2*space_between_buttons,
                              'width' : display_width  *(6/20)-space_between_buttons,
                              'height': display_width     *(2/20),
                              'action': credits_loop             } ,
               'Easy'       :{'x'     : display_width   *(7/20)-space_between_buttons/2,
                              'y'     : display_height    *(9/20),
                              'width' : display_width  *(6/20)-space_between_buttons,
                              'height': display_width     *(2/20),
                              'action': game_loop                } ,
               'Normal'     :{'x'     : display_width  *(13/20)+space_between_buttons/2,
                              'y'     : display_height    *(9/20),
                              'width' : display_width  *(6/20)-space_between_buttons,
                              'height': display_width     *(2/20),
                              'action': game_loop                } ,
               'Hard'       :{'x'     : display_width   *(7/20)-space_between_buttons/2,
                              'y'     : display_height   *(11/20)+2*space_between_buttons,
                              'width' : display_width  *(6/20)-space_between_buttons,
                              'height': display_width     *(2/20),
                              'action': game_loop                } ,
               'Diabolical' :{'x'     : display_width  *(13/20)+space_between_buttons/2,
                              'y'     : display_height   *(11/20)+2*space_between_buttons,
                              'width' : display_width  *(6/20)-space_between_buttons,
                              'height': display_width     *(2/20),
                              'action': game_loop                } ,
              'Instructions':{'x'     : display_width    *(7/20)-space_between_buttons/2,
                              'y'     : display_height   *(13/20)+4*space_between_buttons,
                              'width' : display_width    *(6/20)-space_between_buttons,
                              'height': display_height   *(2 /20),
                              'action': instructions_loop               } ,
              'Two Player'  :{'x'     : display_width    *(13/20)+space_between_buttons/2,
                              'y'     : display_height   *(13/20)+4*space_between_buttons,
                              'width' : display_width    *(6/20)-space_between_buttons,
                              'height': display_height   *(2 /20),
                              'action': game_loop               } }

    return buttons

def create_button(x , y, width, height, colour = red, hover_colour = white, text = 'hello', text_colour = black, action = None, number_of_things = 0, number_of_players = 1):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width/2 > mouse[0] > x - width/2 and y + height/2 > mouse[1] > y - height/2:
        pygame.draw.rect(game_display, hover_colour, (x-width/2,y-height/2,width,height))
        if click[0] == 1 and action != None:
            time.sleep(0.2)
            if number_of_things != 0:
                action(number_of_things = number_of_things, number_of_players = number_of_players)
            else:
                # For basic acions like "main menu", "Highscores", "Credits"
                action()

    else:
        pygame.draw.rect(game_display, colour, (x-width/2,y-height/2,width,height))
    message_display(text = text, position = (x,y), colour = text_colour)

def intro_loop(intro = True):
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                save_scores(score_data)
                quit()

        game_display.fill(black)
        message_display(text = 'Space Dodge', position = title, text_size = 50)

        create_button(buttons['Play']['x'], buttons['Play']['y'], buttons['Play']['width'], buttons['Play']['height'], text = 'Play', action = buttons['Play']['action'])

        create_button(buttons['Highscores']['x'], buttons['Highscores']['y'], buttons['Highscores']['width'], buttons['Highscores']['height'], text = 'Highscores', action = buttons['Highscores']['action'])

        create_button(buttons['Credits']['x'], buttons['Credits']['y'], buttons['Credits']['width'], buttons['Credits']['height'], text = 'Credits', action = buttons['Credits']['action'])

        create_button(buttons['Two Player']['x'], buttons['Two Player']['y'], buttons['Two Player']['width'], buttons['Two Player']['height'], text = 'Two Player', action = buttons['Two Player']['action'])

        create_button(buttons['Instructions']['x'], buttons['Instructions']['y'], buttons['Instructions']['width'], buttons['Instructions']['height'], text = 'Instructions', action = buttons['Instructions']['action'])

        pygame.display.update()
        clock.tick(60)
    intro = False

def instructions_loop(instructions = True):
    while instructions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                save_scores(score_data)
                quit()

        game_display.fill(black)
        message_display(text = 'Instructions', position = title, text_size = 50)

        message_display(text = 'This is you:', position = (display_width*(9/20),display_height*(6/20)), text_size = 20)
        game_display.blit(icon, (display_width*(12/20),display_height*(6/20)-17))

        message_display(text = 'Avoid these:', position = (display_width*(9/20),display_height*(7.5/20)), text_size = 20)
        pygame.draw.rect(game_display, white, [display_width*(12/20), display_height*(7.5/20)-17, 30, 30])

        message_display(text = 'Arrow keys to move', position = (display_width/2,display_height*(9/20)), text_size = 20)
        message_display(text = '(w,a,s,d for second player)', position = (display_width/2,display_height*(10/20)), text_size = 20)
        message_display(text = 'Space bar to pause', position = (display_width/2,display_height*(11/20)), text_size = 20)
        message_display(text = 'Enter to play again', position = (display_width/2, display_height*(12/20)), text_size = 20)
        #message_display(text = 'Harley Taylor while tommy fiddle his diddle ', position = (display_width/2, display_height*(10.5/20)), text_size = 20)

        create_button(buttons['Main Menu']['x'], buttons['Main Menu']['y'], buttons['Main Menu']['width'], buttons['Main Menu']['height'], text = 'Main Menu', action = buttons['Main Menu']['action'])

        pygame.display.update()
        clock.tick(60)
    instructions = False

def twoplay_loop(twoplayer = True):
    while twoplayer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                save_scores(score_data)
                quit()

        game_display.fill(black)
        message_display(text = 'Two players', position = title, text_size = 50)

        create_button(buttons['Easy']['x'], buttons['Easy']['y'], buttons['Easy']['width'], buttons['Easy']['height'], text = 'Easy', action = buttons['Easy']['action'], number_of_things = 4, number_of_players = 2)

        create_button(buttons['Normal']['x'], buttons['Normal']['y'], buttons['Normal']['width'], buttons['Normal']['height'], text = 'Normal', action = buttons['Normal']['action'], number_of_things = 8, number_of_players = 2)

        create_button(buttons['Hard']['x'], buttons['Hard']['y'], buttons['Hard']['width'], buttons['Hard']['height'], text = 'Hard', action = buttons['Hard']['action'], number_of_things = 12, number_of_players = 2)

        create_button(buttons['Diabolical']['x'], buttons['Diabolical']['y'], buttons['Diabolical']['width'], buttons['Diabolical']['height'], text = 'Diabolical', action = buttons['Diabolical']['action'], number_of_things = 20, number_of_players = 2)

        create_button(buttons['Main Menu']['x'], buttons['Main Menu']['y'], buttons['Main Menu']['width'], buttons['Main Menu']['height'], text = 'Main Menu', action = buttons['Main Menu']['action'])

        pygame.display.update()
        clock.tick(60)
    twoplayer = False

def play_loop(settings = True):
    while settings == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                save_scores(score_data)
                quit()
        game_display.fill(black)

        message_display(text = 'Choose Difficulty', position = title, text_size = 50)

        create_button(buttons['Easy']['x'], buttons['Easy']['y'], buttons['Easy']['width'], buttons['Easy']['height'], text = 'Easy', action = buttons['Easy']['action'], number_of_things = 4)

        create_button(buttons['Normal']['x'], buttons['Normal']['y'], buttons['Normal']['width'], buttons['Normal']['height'], text = 'Normal', action = buttons['Normal']['action'], number_of_things = 8)

        create_button(buttons['Hard']['x'], buttons['Hard']['y'], buttons['Hard']['width'], buttons['Hard']['height'], text = 'Hard', action = buttons['Hard']['action'], number_of_things = 12)

        create_button(buttons['Diabolical']['x'], buttons['Diabolical']['y'], buttons['Diabolical']['width'], buttons['Diabolical']['height'], text = 'Diabolical', action = buttons['Diabolical']['action'], number_of_things = 20)

        create_button(buttons['Main Menu']['x'], buttons['Main Menu']['y'], buttons['Main Menu']['width'], buttons['Main Menu']['height'], text = 'Main Menu', action = buttons['Main Menu']['action'])

        pygame.display.update()
        clock.tick(60)

def highscores_loop(highscore = True):
    while highscore == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                save_scores(score_data)
                quit()
        game_display.fill(black)

        message_display(text = 'Highscores', position = title, text_size = 50)

        for n, mode in enumerate(['Easy','Normal','Hard','Diabolical']):
            message_display(text = mode, position = (display_width*((5+3.25*n)/20),display_height*(7/20)), text_size = 20)
            for number, score in enumerate(score_data[mode], start = 1):
                message_display(text = str(score), position = (display_width*((5+3.25*n)/20),display_height*((13-number)/20)), text_size = 20)

        create_button(buttons['Main Menu']['x'], buttons['Main Menu']['y'], buttons['Main Menu']['width'], buttons['Main Menu']['height'], text = 'Main Menu', action = buttons['Main Menu']['action'])

        pygame.display.update()
        clock.tick(60)
    highscore == False

def credits_loop(credits = True):
    while credits:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                save_scores(score_data)
                quit()
        game_display.fill(black)
        message_display(text = 'Credits', position = title, text_size = 50)
        message_display(text = 'Space Dodge', position = (display_width/2,display_height*(7.5/20)), text_size = 20)
        message_display(text = 'Created on Python', position = (display_width/2,display_height*(8.5/20)), text_size = 20)
        message_display(text = 'Anthony Dunford', position = (display_width/2, display_height*(10.5/20)), text_size = 20)
        #message_display(text = 'Harley Taylor while tommy fiddle his diddle ', position = (display_width/2, display_height*(10.5/20)), text_size = 20)
        message_display(text = 'December 2017', position = (display_width/2, display_height*(11.5/20)), text_size = 20)

        create_button(buttons['Main Menu']['x'], buttons['Main Menu']['y'], buttons['Main Menu']['width'], buttons['Main Menu']['height'], text = 'Main Menu', action = buttons['Main Menu']['action'])

        pygame.display.update()
        clock.tick(60)

def gameover_loop(number_of_things, score_data, post_game_message = '', gameover = True):
    while gameover:
        message_display('Game Over', text_size = 50, position = title, colour = cyan)

        if post_game_message != '':
            pygame.draw.rect(game_display, black, (display_width*(6/20),display_height*(5.5/20),display_width*(6.5/20),display_height*(2/20)))
            message_display(post_game_message, text_size = 20, position = (display_width*(10/20),display_height*(6.5/20)), colour = yellow)

        create_button(display_width/2, display_height*(4.5/10), display_height/2, display_width/10, text = 'Play Again (Enter)', action = game_loop, number_of_things = number_of_things)

        create_button(display_width/2, display_height*(6/10), display_width/2, display_width/10, text = 'Main Menu', action = intro_loop)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop(number_of_things = number_of_things)
            if event.type == pygame.QUIT:
                save_scores(score_data)
                quit()
                exit_game == True

def game_loop(game_start_speed = 100, pause = False, game_over = False, paused_time = 0, number_of_things = 8, number_of_players = 1):
    game_speed = game_start_speed
    start_time = time.time()
    exit_game = False

    all_things = range(0,number_of_things)
    direction_list = ['up','down','left','right']

    t = initialise_things(all_things,direction_list)

    player_x = []
    player_y = []
    player_x_change = []
    player_y_change = []
    for n in range(0,number_of_players):
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

                if number_of_players == 2:
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

                if number_of_players == 2:
                    if event.key == pygame.K_a:
                        player_x_change[1] = 0
                    if event.key == pygame.K_d:
                        player_x_change[1] = 0
                    if event.key == pygame.K_w:
                        player_y_change[1] = 0
                    if event.key == pygame.K_s:
                        player_y_change[1] = 0

        if game_over == True:
            if number_of_players == 1:
                score_data, new_highscore = record_scores(score = str(alive_time), number = number_of_things)
                if new_highscore == True:
                    gameover_loop(score_data = score_data, number_of_things = number_of_things, post_game_message = 'New Highscore...!')
                else:
                    gameover_loop(score_data = score_data, number_of_things = number_of_things)
            elif number_of_players == 2:
                gameover_loop(number_of_things = number_of_things, post_game_message = '')
        else:
            if pause == False:

                current_time = time.time()
                game_display.fill(black)

                for thing in all_things:
                    t['x'][thing], t['y'][thing], t['delay'][thing] = move_thing(t['direction'][thing], t['x'][thing], t['y'][thing], t['height'][thing], t['width'][thing], t['speed'][thing], t['delay'][thing])
                    display_thing(t['x'][thing], t['y'][thing], t['width'][thing], t['height'][thing], white)

                for n in range(0,number_of_players):
                    player_x[n] += player_x_change[n]
                    player_y[n] += player_y_change[n]
                    game_display.blit(player_image[n], (player_x[n],player_y[n]))

                    # Crash into side of screen
                    if player_x[n] > display_width - player_width or player_x[n] < 0 or player_y[n] > display_height - player_height or player_y[n] < 0:
                        game_over = True
                    #Crash into things
                    for thing in all_things:
                        if player_x[n] - t['width'][thing] < t['x'][thing] and t['x'][thing] < player_x[n] + player_width and player_y[n] - t['height'][thing] < t['y'][thing] and t['y'][thing] < player_y[0] + player_height:
                            game_over = True

                alive_time = round(current_time-start_time-paused_time,1)
                clock.tick(game_speed)
                game_speed = game_start_speed + 2*round(current_time-start_time-paused_time)

                message_display(str(alive_time), text_size = 20, position = ((25),(25)), colour = cyan)
                message_display(str(game_speed), text_size = 20, position = ((display_width-25),(25)), colour = cyan)
                pygame.display.update()

            elif pause == True:
                message_display('Paused',50, position = ((display_width/2),(display_height/2)), colour = cyan)
                create_button(buttons['Main Menu']['x'], buttons['Main Menu']['y'], buttons['Main Menu']['width'], buttons['Main Menu']['height'], text = 'Main Menu', action = buttons['Main Menu']['action'])
                pygame.display.update()

score_data = load_scores()
buttons = initialise_buttons()
intro_loop()
