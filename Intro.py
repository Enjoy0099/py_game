import pygame, time, random
from pygame.locals import *
from pytmx.util_pygame import load_pygame
import C_H

def blit_my_map(window, tmxdata, world_offset):

    for tile in tmxdata.layers[0].tiles():
        img = pygame.transform.scale(tile[2], (35,35))                       
        x_pixel = tile[0] * 35 + world_offset[0]                       
        y_pixel = tile[1] * 35 + world_offset[1]                       
        window.blit(img, (x_pixel, y_pixel) )



def get_my_tiles_properties(tmxdata, x, y, world_offset):

    world_x = x - world_offset[0]
    world_y = y - world_offset[1]
    tile_x = world_x // 35
    tile_y = world_y // 35
    properties = tmxdata.get_tile_properties(tile_x, tile_y, 0)
    if properties is None:
        properties = {"id": -1, "climbable": False, "ground": False, "health": 0, "points": 0, 
                      "provide": "", "require": "", "solid": False}
    properties["x"] = tile_x
    properties["y"] = tile_y
    return properties




def main():

    font = pygame.font.SysFont("font/Viga-Regular.ttf", 40)      # import font and apply size
    tmx_data = load_pygame("Intro.tmx")




    pygame.mixer.music.load("sounds/intro_game_0.wav")
    pygame.mixer.music.play(1)
    jump_sfx = pygame.mixer.Sound("sounds/jump.wav")
    Game_begin = pygame.mixer.Sound("sounds/Start_sound.wav")



    UFO = pygame.image.load("imges/UFO (1).png")
    UFO_Crash = pygame.image.load("imges/UFO Crash (1).png")
    Game_Name = pygame.image.load("imges/Banner (1).png")
    intro_Start = 19 * 3
    intro_Start_0 = 19 * 3
    intro_Start_1 = 19 * 3
    can_not_move = 1





    y_ground = window.get_height() - 200
    x = 0
    y = y_ground
    world_offset = [-120,-100]



    quit = False




    stand = 0




    player_stand = pygame.image.load("assets/p2_stand.png").convert_alpha()
    player_stand = pygame.transform.scale(player_stand, (50,70))
    player_stand_left = pygame.transform.flip(player_stand, True, False)

    player_right = [
        pygame.image.load("assets/p2_walk/PNG/p2_walk01.png").convert_alpha(),
        pygame.image.load("assets/p2_walk/PNG/p2_walk02.png").convert_alpha(),
        pygame.image.load("assets/p2_walk/PNG/p2_walk03.png").convert_alpha(),
        pygame.image.load("assets/p2_walk/PNG/p2_walk04.png").convert_alpha(),
        pygame.image.load("assets/p2_walk/PNG/p2_walk05.png").convert_alpha(),
        pygame.image.load("assets/p2_walk/PNG/p2_walk06.png").convert_alpha(),
        pygame.image.load("assets/p2_walk/PNG/p2_walk07.png").convert_alpha(),
        pygame.image.load("assets/p2_walk/PNG/p2_walk08.png").convert_alpha(),
        pygame.image.load("assets/p2_walk/PNG/p2_walk09.png").convert_alpha(),
        pygame.image.load("assets/p2_walk/PNG/p2_walk10.png").convert_alpha(),
        pygame.image.load("assets/p2_walk/PNG/p2_walk11.png").convert_alpha()
    ]
    player_right = [pygame.transform.scale(image, (50,70)) for image in player_right]
    player_right_frame = 0  

    player_left = [pygame.transform.flip(image, True, False) for image in player_right]
    player_left_frame = 0

    player_jump = pygame.image.load("assets/p2_jump.png").convert_alpha()
    player_jump = pygame.transform.scale(player_jump, (50,70))
    player_jump_left = pygame.transform.flip(player_jump, True, False)
    player_jump_frame = 0

    player_land = pygame.image.load("assets/p2_duck.png").convert_alpha()
    player_land = pygame.transform.scale(player_land, (50,70))
    player_land_left = pygame.transform.flip(player_land, True, False)





    direction = "stand"
    



    while not quit:

        window.fill((214,223,224))




        blit_my_map(window, tmx_data, world_offset)





        standing_on_left = get_my_tiles_properties(tmx_data, x + 15, y + 70, world_offset)
        standing_on_right = get_my_tiles_properties(tmx_data, x + 50 - 15, y + 70, world_offset)





        keyspressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit = True






        if can_not_move:
            if keyspressed[ord("a")]:
                left_tile_up = get_my_tiles_properties(tmx_data, x - 10, y + 10, world_offset)
                left_tile_down = get_my_tiles_properties(tmx_data, x - 10, y + 55, world_offset)
                stand = 1
                if not left_tile_up["solid"] and not left_tile_down["solid"]: 
                    direction = "left"
                    x = x - 10
            if keyspressed[ord("d")]:
                right_tile_up = get_my_tiles_properties(tmx_data, x + 50 + 10, y + 10, world_offset)
                right_tile_down = get_my_tiles_properties(tmx_data, x + 50 + 10, y + 55, world_offset)
                stand = 0
                if not right_tile_up["solid"] and not right_tile_down["solid"]:
                    direction = "right"
                    x = x + 10
            if keyspressed[ord("w")]:
                if standing_on_left["ground"] == True or standing_on_right["ground"] == True:
                    jump_sfx.play()
                    player_jump_frame = 10
            if sum(keyspressed) == 0:
                direction = "stand"
        above_tile_left = get_my_tiles_properties(tmx_data, x + 25 - 15, y - 10, world_offset)
        above_tile_right = get_my_tiles_properties(tmx_data, x + 25 + 15, y - 10, world_offset)
        if above_tile_right["solid"] or above_tile_left["solid"]:
            player_jump_frame = 0
        if player_jump_frame > 0:
            y = y - 10
            direction = "jump"
            player_jump_frame = player_jump_frame - 1
        elif (standing_on_left["ground"] == False and standing_on_right["ground"] == False):
            y = y + 10
            direction = "landing"
        



        if standing_on_right["x"] == 48:
            can_not_move = 0
            window.blit(Game_Name, (0,0))
            intro_Start -= 1
            if intro_Start <= 0:
                window.blit(UFO, (0,0))
                intro_Start_0 -= 1
            if intro_Start_0 <= 0:
                window.blit(UFO_Crash, (0,0))
                intro_Start_1 -= 1
                if intro_Start_1 == 19:
                    Game_begin.play()
            if intro_Start_1 <= 0:
                quit = True

            




        
        if x < 360:
            x = 360
            world_offset[0] += 10
        if x > window.get_width() - 50 - 360:
            x = window.get_width() - 50 - 360
            world_offset[0] -= 10
        if y < 160:
            y = 160
            world_offset[1] += 10
        if y > y_ground:
            y = y_ground
            world_offset[1] -= 10
            




        if can_not_move:
            if direction == "left":
                window.blit(player_left[player_left_frame], (x,y))
                player_left_frame = (player_left_frame + 1) % len(player_right)
            elif direction == "right":
                window.blit(player_right[player_right_frame], (x,y))
                player_right_frame = (player_right_frame + 1) % len(player_right)
            elif stand == 1:
                if direction == "jump":
                    window.blit(player_jump_left, (x,y))
                elif direction == "landing":
                    window.blit(player_land_left, (x,y))
                else:
                    window.blit(player_stand_left, (x,y))
            else:
                if direction == "jump":
                    window.blit(player_jump, (x,y))  
                elif direction == "landing":
                    window.blit(player_land, (x,y))
                else:
                    window.blit(player_stand, (x,y))


        pygame.display.update()                        
        clock.tick(19)


#*****************************  Level_00  ************************************

width, height = 1440, 720                          
pygame.init()                                       
pygame.mixer.init()                                 
window = pygame.display.set_mode((width, height))   
pygame.display.set_caption("Baby Blue")
clock = pygame.time.Clock()                     
main()
pygame.quit()