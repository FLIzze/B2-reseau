import pygame
import json
from pygame.locals import *
import gc
import time
import random
from player import Player
import character
from collisionsMap import * 
from collision import * 
from background import *

pygame.init()
pygame.font.init()
font = pygame.font.Font("./font/DeterminationMono.ttf", 45)
pygame.display.set_caption("revenge on inove")

screen = pygame.display.set_mode((1920, 1080))
height = screen.get_height()
width = screen.get_width()

#size of each tile
tileSize = 16
#the zoomlevel exported from tiled
zoomMapLevel = 4
bg = ""
background = Background()
current_dialogue = 0
current_enemy = 0

FPS = 144

#text = ["on va tester les dialogues", "oui"]
charac = character.Main_charac("main charac")
player = Player(width/2, height/2)
playerSprite = (pygame.image.load(player.imgSrc)).convert_alpha()
playerSprite_rect = playerSprite.get_rect()
playerSprite = pygame.transform.scale(playerSprite, (playerSprite_rect.width*zoomMapLevel, playerSprite_rect.height*zoomMapLevel))

def dialogues():
    global current_dialogue
    with open('./dialogues.json', 'r') as dialogue:
        data = json.load(dialogue)

    text = data[current_dialogue]["dialogue"]

    #draw the white outter line from dialogue
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(width-width/1.17, height-height/3.2, width-width/3.4, height-height/1.3))
    #draw the black inner line
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(width-width/1.178, height-height/3.31, width-width/3.26, height-height/1.265))
    #draw the character face
    #pygame.draw.rect(screen, "green", pygame.Rect(width-width/1.19, height-height/3.44, width-width/1.1, height-height/1.2))

    text_y_position = width-width/1.67
    text_x_position = width-width/1.2

    index = 0
    text_return = ''
    for i in text:
        index +=1
        if i == ' ' and index >= 40:
            index = 0
            text_return += '\n'
        else:
            text_return += i

    text_arr = text_return.split("\n")

    #allow to have multiple lines of dialogue
    i = 0
    for line in text_arr:
        if i == 5:
            time.sleep(0.01)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(width-width/1.178, height-height/3.31, width-width/3.26, height-height/1.265))
            text_y_position = width-width/1.67
            text_x_position = width-width/1.2
            i = 0
        for char in line:
            text_surface = font.render(char, True, (255, 255, 255))
            text_rect = (text_x_position, text_y_position)
            time.sleep(0.04)
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            text_x_position+= width-width/1.014
        text_x_position = width-width/1.2
        text_y_position += width-width/1.02
        i += 1
    time.sleep(1)
    current_dialogue+=1

def info():
    #display all the info at the top of the screen
    text_info = "Press e to show dialogue, arrows to move"
    text_surface = font.render(text_info, True, (255, 255, 255))
    text_rect = (0, 0)
    screen.blit(text_surface, text_rect)

def move():
    moveX = 0
    moveY = 0
    global pressed_l
    global pressed_r
    global pressed_u
    global pressed_d
    global movable
    global before_last_key
    global last_key
    movable = True
    tmp_key = last_key

    if last_key == 'left':
        player.frameX = 6*16
        player.animate(pressed_l)
    if last_key == 'right':
        player.frameX = 2*16
        player.animate(pressed_r)
    if last_key == 'up':
        player.frameX = 0*16
        player.animate(pressed_u)
    if last_key == 'down':
        player.frameX = 4*16
        player.animate(pressed_d)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        last_key = 'left'
        pressed_l = True
        moveX = 1+player.sprint
        for i in Collision.allCollisions:
            if (check_collisions('left', i)):
                movable = False
    else:
        pressed_l = False
        
    if keys[pygame.K_RIGHT]:
        last_key = 'right'
        pressed_r = True
        moveX = -1-player.sprint
        for i in Collision.allCollisions:
            if (check_collisions('right', i)):
                movable = False
    else:
        pressed_r = False

    if keys[pygame.K_UP]:
        last_key = 'up'
        pressed_u = True
        moveY = 1+player.sprint
        for i in Collision.allCollisions:
            if (check_collisions('up', i)):
                movable = False
    else:
        pressed_u = False

    if keys[pygame.K_DOWN]:
        last_key = 'down'
        pressed_d = True
        moveY = -1-player.sprint
        for i in Collision.allCollisions:
            if (check_collisions('bottom', i)):
                movable = False
    else:
        pressed_d = False

    if movable:
        player.position_y -= moveY
        player.position_x -= moveX
        background.x += moveX
        background.y += moveY
        for i in Collision.allCollisions:
            i.y += moveY
            i.x += moveX 

    if (tmp_key != last_key):
        before_last_key = tmp_key 

    if keys[pygame.K_SPACE]:
        player.sprint = 1.1
    else:
        player.sprint = 0

def check_collisions(direction: str, collision: Collision):
    if direction == 'left':
        if (player.position_x-4*tileSize <= collision.fixedX+collision.size and
            player.position_x + player.width >= collision.fixedX and
            player.position_y + player.height + 2.3*tileSize >= collision.fixedY and
            player.position_y - 2.3*tileSize<= collision.fixedY + collision.size):
            if collision.id != 126 and collision.id != 0:
                check_fight(collision)
            else:
                return True
    elif direction == 'right':
        if (player.position_x <= collision.fixedX+collision.size and
            player.position_x + player.width+4*tileSize >= collision.fixedX and
            player.position_y + player.height + 2.3*tileSize >= collision.fixedY and
            player.position_y - 2.3*tileSize <= collision.fixedY + collision.size):
            if collision.id != 126 and collision.id != 0:
                check_fight(collision)
            else:
                return True
    elif direction == 'up':
        if (player.position_x - 3.5*tileSize <= collision.fixedX+collision.size and
            player.position_x + player.width + 3.5*tileSize >= collision.fixedX and
            player.position_y + player.height>= collision.fixedY and
            player.position_y -3*tileSize<= collision.fixedY + collision.size):
            if collision.id != 126 and collision.id != 0:
                check_fight(collision)
            else:
                return True
    elif direction == 'bottom':
        if (player.position_x - 3.5*tileSize <= collision.fixedX+collision.size and
            player.position_x + player.width + 3.5*tileSize >= collision.fixedX and
            player.position_y + player.height +3*tileSize>= collision.fixedY and
            player.position_y<= collision.fixedY + collision.size):
            if collision.id != 126 and collision.id != 0:
                check_fight(collision)
            else:
                return True
    return False 

def check_fight(collision):
    if not collision.used:
        id = collision.id
        for i in Collision.allCollisions:
            if i.id == id:
                i.used = True
        dialogues()
        for i in range(0, height+height//20, height//20):
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, width, i))
            time.sleep(0.05)
            pygame.display.flip()
        start_fight()

def main():
    clock = pygame.time.Clock()
    load_map("img/floor0.png")
    dialogues()

    while True:
        #load_map()
        #re fill the whole screen therefore makes it refresh every frame
        screen.fill('black')
        #limit frames by 144 atm
        clock.tick(FPS)

        #quit the game if f4
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        #fill the screen with background image at x, y
        screen.blit(bg, (background.x-background.offset['x'], background.y-background.offset['y']))
        #draw the player (just a red circle atm)
        #pygame.draw.circle(screen, "green", player_pos, 20)

        #draw every collision
        #for i in Collision.allCollisions:
            #print(i.fixedX, i.fixedY, player.position_x, player.position_y)
            #pygame.draw.circle(screen, "red", (i.x,i.y), 16)

        #display info text
        #info()
        #get inputs and move the char
        screen.blit(playerSprite, (width/2, height/2), (player.frameX*zoomMapLevel, player.frameY*zoomMapLevel, player.width*zoomMapLevel, player.height*zoomMapLevel))
        move()
        #print(player.position_x, player.position_y)
        #apply all the blit
        check_if_elevator_near()
        if selection:
            skin_selection()

        pygame.display.flip()

def load_map(imgSrc: str):
    global bg

    background.imgSrc = imgSrc 
    bg = (pygame.image.load(background.imgSrc)).convert_alpha()

 
    if background.current_floor == 0:
        background.offset = {
            'x': 55.5*tileSize*zoomMapLevel,
            'y': 50*tileSize*zoomMapLevel
        }
        collisionsArray = collision_floor0()
    elif background.current_floor == 1:
        background.offset = {
            'x': 90.5*tileSize*zoomMapLevel,
            'y': 56*tileSize*zoomMapLevel
        }
        collisionsArray = collision_floor1()
    elif background.current_floor == 2:
        background.offset = {
            'x': 90.5*tileSize*zoomMapLevel,
            'y': 56*tileSize*zoomMapLevel
        }
        collisionsArray = collision_floor2()
    else:
        collisionsArray = []


    #2dArray witl all collisions
    collisionsMap = [int]

    #Make 1d to 2dArray
    for i in range(0, len(collisionsArray), 150):
        collisionsMap.append(collisionsArray[0+i: 151+i])

    del Collision.allCollisions[:]

    #create instance of all collision
    for i in range(1, len(collisionsMap), 1):
        for j in range(0, 150, 1):
            if (collisionsMap[i][j] == 257):
                Collision((j)*zoomMapLevel*tileSize-background.offset['x'], (i-1.3)*zoomMapLevel*tileSize-background.offset['y'], 257)
            elif (collisionsMap[i][j] == 258):
                Collision((j)*zoomMapLevel*tileSize-background.offset['x'], (i-1.3)*zoomMapLevel*tileSize-background.offset['y'], 258)
            elif (collisionsMap[i][j] == 259):
                Collision((j)*zoomMapLevel*tileSize-background.offset['x'], (i-1.3)*zoomMapLevel*tileSize-background.offset['y'], 259)
            elif (collisionsMap[i][j] == 260):
                Collision((j)*zoomMapLevel*tileSize-background.offset['x'], (i-1.3)*zoomMapLevel*tileSize-background.offset['y'], 260)
            elif (collisionsMap[i][j] == 261):
                Collision((j)*zoomMapLevel*tileSize-background.offset['x'], (i-1.3)*zoomMapLevel*tileSize-background.offset['y'], 261)
            elif (collisionsMap[i][j] == 262):
                Collision((j)*zoomMapLevel*tileSize-background.offset['x'], (i-1.3)*zoomMapLevel*tileSize-background.offset['y'], 262)
            elif (collisionsMap[i][j] == 263):
                Collision((j)*zoomMapLevel*tileSize-background.offset['x'], (i-1.3)*zoomMapLevel*tileSize-background.offset['y'], 263)
            elif (collisionsMap[i][j] == 264):
                Collision((j)*zoomMapLevel*tileSize-background.offset['x'], (i-1.3)*zoomMapLevel*tileSize-background.offset['y'], 264)
            elif (collisionsMap[i][j] == 265):
                Collision((j)*zoomMapLevel*tileSize-background.offset['x'], (i-1.3)*zoomMapLevel*tileSize-background.offset['y'], 265)
            elif (collisionsMap[i][j] == 266):
                Collision((j)*zoomMapLevel*tileSize-background.offset['x'], (i-1.3)*zoomMapLevel*tileSize-background.offset['y'], 266)
            elif (collisionsMap[i][j] == 126):
                Collision((j)*zoomMapLevel*tileSize-background.offset['x'], (i-1.3)*zoomMapLevel*tileSize-background.offset['y'])

def floor_selection():
    global font
    text = ""
    keys2 = pygame.key.get_pressed()
    if background.current_floor == 0:
        text = ["Quel étage ?", "   > RDC", "     1"]
        if keys2[pygame.K_2]:
            background.current_floor = 1
            load_map("img/floor1.png")
    elif background.current_floor == 1:
        text = ["Quel étage ?", "   > 1", "     2"]
        if keys2[pygame.K_3]:
            background.current_floor = 2
            load_map("img/floor2.png")
    else:
        return False

    text_y_position = width-width/1.28
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(width-width/2.95, height-height/1.58, width-width/1.218, height-height/1.22))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(width-width/3, height-height/1.6, width-width/1.2, height-height/1.194))

    for line in text:
        text_surface = font.render(line, True, (255, 255, 255))
        text_rect = (width-width/3.1, text_y_position)
        screen.blit(text_surface, text_rect)
        text_y_position += width-width/1.02

    font2 = pygame.font.Font("./font/DeterminationMono.ttf", 35)
    if background.current_floor == 0:
        text_select = "1\n2"
    elif background.current_floor == 1:
        text_select = "2\n3"
    else:
        return False
    
    selection_text = text_select.split("\n")
    selection_y = height-height/1.75
        
    for line in selection_text:
        text_surface = font2.render(line, True, "yellow")
        text_rect = (width-width/3.3, selection_y)
        screen.blit(text_surface, text_rect)
        selection_y += height-height/1.037

def skin_selection():
    global selection
    screen.fill('black')
    text_surface = font.render("Selectionnez votre personnage:", True, (255, 255, 255))
    text_rect = (width-width/1.48, height-height/1.5)
    text_surface_selection = font.render("1  2  3", True, 'yellow')
    text_rect_selection =(width-width/1.85, height-height/1.8)
    playerSprite = (pygame.image.load(player.imgSrc)).convert_alpha()
    playerSprite_rect = playerSprite.get_rect()
    playerSprite = pygame.transform.scale(playerSprite, (playerSprite_rect.width*zoomMapLevel, playerSprite_rect.height*zoomMapLevel))
    screen.blit(text_surface, text_rect)
    screen.blit(text_surface_selection, text_rect_selection)
    screen.blit(playerSprite, (width/2.06-player.width*zoomMapLevel, height/2), (4*zoomMapLevel*player.width, 2*player.height*zoomMapLevel, tileSize*zoomMapLevel, player.height*zoomMapLevel))
    screen.blit(playerSprite, (width/2.06, height/2), (4*zoomMapLevel*player.width, 6*player.height*zoomMapLevel, tileSize*zoomMapLevel, player.height*zoomMapLevel))
    screen.blit(playerSprite, (width/2.06+player.width*zoomMapLevel, height/2), (4*zoomMapLevel*player.width, 10*player.height*zoomMapLevel, tileSize*zoomMapLevel, player.height*zoomMapLevel))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        player.char = 1
        player.frameY = 24
        selection = False
    elif keys[pygame.K_2]:
        player.char = 2
        player.frameY = 24*5
        selection = False
    elif keys[pygame.K_3]:
        player.char = 3
        player.frameY = 24*9
        selection = False
    pygame.display.flip()

def check_if_elevator_near():
    global near_escalator
    if background.current_floor == 2:
        return False
    if (player.position_x > -144 and player.position_x < 21 and player.position_y < -200 and player.position_y > -324 and current_enemy == 3 and background.current_floor == 0) or (current_enemy == 6 and background.current_floor == 1 and player.position_x > -144 and player.position_x < 21 and player.position_y < -200 and player.position_y > -324): 
        text_surface = font.render("[e]", True,"yellow") 
        text_rect = (width/2-player.width/2, height/2+height-height/0.98)
        screen.blit(text_surface, text_rect)
        keys2 = pygame.key.get_pressed()
        if keys2[pygame.K_e]:
            near_escalator = True
        if near_escalator == True: 
            floor_selection()
    else:
        near_escalator = False

fight_data = [character.Student(), "coffee", character.Depressed_student(), "rope", character.School_referent(), "trello", character.Mentor(), "wooclap", character.Teacher(), "survey_monkey", character.Director(), "mug_inove", character.Mentor2(), "", character.Mentor3(), "shell", character.Network_teacher(), ""]

def start_fight():
    fight = True
    text = ""
    global current_enemy
    enemy = fight_data[current_enemy*2]
    if enemy.get_name() == "network teacher":
        charac.reset_health()
    elif enemy.get_name() == "mentor" or enemy.get_name() == "mentor 2":
        charac.up_level()

    charac_items = charac.list_items_array()
    enemy_items = enemy.list_items_array()
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(width/40, height/13, width-width/1.2, height/1.22))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(width/4, height/2-height/5, width/1.5, height/2.88))
        
    if text == "":
        text = f"Choose an item, 1-{(len(charac_items))}"

    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (width/4, height/2-height/5))
                    
    y_pos = height/13
    j = 1
    for i in charac_items:
        text_surface = font.render(i, True, (0, 0, 0))
        screen.blit(text_surface, (width//40, y_pos))
        select_number = font.render(str(j), True, "yellow")
        screen.blit(select_number, (width//100, y_pos))
        y_pos+=height//40
        j+=1

    hp_charac_surface = font.render(charac.health(), True, (40, 150, 10))
    hp_enemy_surface = font.render(enemy.health(), True, "red")
    hp_charac_rect = (width/2, height/1.3)
    hp_enemy_rect = (width/2, height/7)

    screen.blit(hp_charac_surface, hp_charac_rect)
    screen.blit(hp_enemy_surface, hp_enemy_rect)
    pygame.display.flip()

    while fight:
        screen.fill("black")

        select_item = True
        while select_item:
            e = pygame.event.wait()
            text_surface = font.render(text, True, (0, 0, 0))
            screen.blit(text_surface, (width/4, height/2-height/5))
            if e.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_1] and len(charac_items) >= 1:
                    item = 0
                    select_item = False
                elif keys[pygame.K_2] and len(charac_items) >= 2:
                    item = 1
                    select_item = False
                elif keys[pygame.K_3] and len(charac_items) >= 3:
                    item = 2
                    select_item = False
                elif keys[pygame.K_4] and len(charac_items) >= 4:
                    item = 3
                    select_item = False
                elif keys[pygame.K_5] and len(charac_items) >= 5:
                    item = 4
                    select_item = False
                elif keys[pygame.K_6] and len(charac_items) >= 6:
                    item = 5
                    select_item = False
                elif keys[pygame.K_7] and len(charac_items) >= 7:
                    item = 6
                    select_item = False
                elif keys[pygame.K_8] and len(charac_items) >= 8:
                    item = 7
                    select_item = False

        damages = charac.inflict_damages(charac_items[int(item)], enemy)
        if damages > 1:
            text = "Tu as infligé "+str(damages)+" dégâts."
        elif damages == 1:
            text = "Tu as infligé 1 dégât."
        elif damages == 0:
            text = "Il ne s'est rien passé."
        elif damages < 0:
            text = "Il t'a contré et t'inflige "+str(damages)+"dégâts."

        if enemy.is_alive() == 0:
            fight = False
        
        randNbr = random.randint(0, len(enemy_items)-1)
        damages = enemy.inflict_damages(enemy_items[randNbr], charac)
        
        text += "\n"
        if damages > 1:
            text += "Il t'a infligé "+str(damages)+" dégâts."
        elif damages == 1:
            text += "Il t'a infligé 1 dégât."
        elif damages == 0:
            text += "Il ne s'est rien passé."
        else:
            text += "Tu l'as contré et lui inflige "+str(damages)+" dégâts."

        i = 0

        text_y_position = height/2-height/5
        text_x_position = width/4
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(width/40, height/13, width-width/1.2, height/1.22))
        hp_charac_surface = font.render(charac.health(), True, (40, 150, 10))
        hp_enemy_surface = font.render(enemy.health(), True, "red")
        hp_charac_rect = (width/2, height/1.3)
        hp_enemy_rect = (width/2, height/7)
        screen.blit(hp_charac_surface, hp_charac_rect)
        screen.blit(hp_enemy_surface, hp_enemy_rect)
        y_pos = height/13
        j = 1
        for i in charac_items:
            text_surface = font.render(i, True, (0, 0, 0))
            screen.blit(text_surface, (width//40, y_pos))
            select_number = font.render(str(j), True, "yellow")
            screen.blit(select_number, (width//100, y_pos))
            y_pos+=height//40
            j+=1

        text_arr = text.split("\n")

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(width/4, height/2-height/5, width/1.5, height/2.88))
        for line in text_arr:
            for char in line:
                text_surface = font.render(char, True, (0, 0, 0))
                text_rect = (text_x_position, text_y_position)
                time.sleep(0.01)
                screen.blit(text_surface, text_rect)
                pygame.display.flip()
                text_x_position+= width-width/1.014
            text_x_position = width/4
            text_y_position += width-width/1.02

        if charac.is_alive() == 0:
            lost()
        elif (enemy.is_alive() == 0) and (enemy.get_name() == "network teacher"):
            won()
        elif enemy.is_alive() == 0:
            charac.add_item(fight_data[(current_enemy*2)+1])
            current_enemy += 1
            if (enemy.get_name() == "school referent") or (enemy.get_name() == "director"):
                dialogues()
                dialogues()
            fight = False

def lost():
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, width, height))
    text_surface = font.render("You lost", True, "red")
    text_rect = (width/2-width/20, height/2-height/20)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(5)
    exit(0)

def won():
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, width, height))
    text_surface = font.render("You won", True, "green")
    text_rect = (width/2-width/20, height/2-height/20)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(5)
    exit(0)


selection = True
movable = True
last_key = ""
before_last_key = ""
pressed_l = False
pressed_r = False
pressed_u = False
pressed_d = False
main()
