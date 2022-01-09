import pygame
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
    tmx_data = load_pygame("Final_map_0.tmx")




    pygame.mixer.music.load("sounds/intro_game_0.wav")
    pygame.mixer.music.play(1)
    coin_sfx = pygame.mixer.Sound("sounds/coin.wav")
    jump_sfx = pygame.mixer.Sound("sounds/jump.wav")
    injury_sfx = pygame.mixer.Sound("sounds/hurt_1.wav")
    key_sfx = pygame.mixer.Sound("sounds/key.wav")
    next_level = pygame.mixer.Sound("sounds/level_increased.wav")
    health_rise = pygame.mixer.Sound("sounds/health.wav")
    level_Complete = pygame.mixer.Sound("sounds/level_Complete.wav")


    time_img = pygame.image.load("imges/Time (1).png").convert_alpha()
    time_img = pygame.transform.scale(time_img, (35,35))
    health_img = pygame.image.load("imges/hea.png").convert_alpha()




    y_ground = window.get_height() - 200
    x = 0
    y = y_ground
    world_offset = [-9800,-9700]    #base(-9800, -9700)  (-7400,-9500)
    R_G = 1

    end_S0 = 0
    button_Time = 19 * 4


    collected_items = []




    quit = False




    stand = 0
    health_wait = 0




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

    time = 120
    every_Second = 20
    health = C_H.health
    



    while not quit:

        window.fill((177,212,224))




        blit_my_map(window, tmx_data, world_offset)


        every_Second -= 1

        if every_Second <= 0:
            time -= 1
            every_Second = 19 


        if time <= 0:
            R_G = 0
            return R_G


        time_show = font.render(f"{time}", 1, (52,25,72))
        health_no_show = font.render(f"{health}", 1, (255,37,17))
        window.blit(health_img, (1, 0))
        window.blit(health_no_show, (40, 5))
        window.blit(time_img, (1330, 4))
        window.blit(time_show, (1370, 9))




        standing_on_left = get_my_tiles_properties(tmx_data, x + 15, y + 70, world_offset)
        standing_on_right = get_my_tiles_properties(tmx_data, x + 50 - 15, y + 70, world_offset)





        keyspressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit = True





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
            above_tile_left = get_my_tiles_properties(tmx_data, x + 25 - 15, y - 10, world_offset)
            above_tile_right = get_my_tiles_properties(tmx_data, x + 25 + 15, y - 10, world_offset)
            if standing_on_left["climbable"] == True or standing_on_right["climbable"] == True:
                y = y - 10 
            if not above_tile_right["solid"] and not above_tile_left["solid"]:
                if standing_on_left["ground"] == True or standing_on_right["ground"] == True:
                    jump_sfx.play()
                    player_jump_frame = 10
            else:
                player_jump_frame = 0
        if keyspressed[ord("s")]:
            if standing_on_left["climbable"] or standing_on_right["climbable"]:
                y = y + 10
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
        elif (standing_on_left["ground"] == False and standing_on_right["ground"] == False) and (standing_on_left["climbable"] == False and standing_on_right["climbable"] == False):
            y = y + 10
            direction = "landing"










        if health_wait != 0:
            health_wait -= 1
        elif (standing_on_left["health"] < 0 or standing_on_right["health"] < 0) and health_wait == 0:
            injury_sfx.play()
            health = health - 1
            if health < 0:
                R_G = 0
                return R_G
            health_wait = 19

        touching_heart_right = get_my_tiles_properties(tmx_data, x + 50 - 6, y + 15, world_offset)
        touching_heart_left = get_my_tiles_properties(tmx_data, x + 6, y + 15, world_offset)
        if touching_heart_right["id"] == 466:
            health = health + touching_heart_right["health"]
            health_rise.play()
            tmx_data.layers[0].data[touching_heart_right["y"]][touching_heart_right["x"]] = 0
        elif touching_heart_left["id"] == 466:
            health = health + touching_heart_left["health"]
            health_rise.play()
            tmx_data.layers[0].data[touching_heart_left["y"]][touching_heart_left["x"]] = 0









        touching_coins_right = get_my_tiles_properties(tmx_data, x + 50 - 6, y + 25, world_offset)
        touching_coins_left = get_my_tiles_properties(tmx_data, x + 6, y + 25, world_offset)
        if touching_coins_right["id"] == 288 or touching_coins_right["id"] == 332:
            tile_x = touching_coins_right["x"]
            tile_y = touching_coins_right["y"]
            coin_sfx.play()
            points = points + touching_coins_right["points"]
            tmx_data.layers[0].data[tile_y][tile_x] = 0  # to remove coin after it is collected
        elif touching_coins_left["id"] == 288 or touching_coins_left["id"] == 332:
            tile_x_left = touching_coins_left["x"]
            tile_y_left = touching_coins_left["y"]  
            coin_sfx.play()
            points = points + touching_coins_left["points"]
            tmx_data.layers[0].data[tile_y_left][tile_x_left] = 0








        
        touching_locks_keys_rightside = touching_coins_right
        touching_locks_keys_leftside = touching_coins_left
        if touching_locks_keys_rightside["provide"] == "green key":
            collected_items.append(touching_locks_keys_rightside["provide"])
            key_sfx.play()
            tmx_data.layers[0].data[touching_locks_keys_rightside["y"]][touching_locks_keys_rightside["x"]] = 0
        elif touching_locks_keys_leftside["provide"] == "green key":
            collected_items.append(touching_locks_keys_leftside["provide"])
            key_sfx.play()
            tmx_data.layers[0].data[touching_locks_keys_leftside["y"]][touching_locks_keys_leftside["x"]] = 0
        if touching_locks_keys_leftside["require"] in collected_items:
            item = touching_locks_keys_leftside["require"]
            if item == "green key":
                tmx_data.layers[0].data[touching_locks_keys_leftside["y"]][touching_locks_keys_leftside["x"]] = 0
                tmx_data.layers[0].data[295][169] = tmx_data.layers[1].data[295][169]
                tmx_data.layers[0].data[296][169] = tmx_data.layers[1].data[296][169]
                next_level.play()
                time = 40





        if standing_on_left["id"] == 254 or standing_on_right["id"] == 254:
            tmx_data.layers[0].data[192][154] = 0
            tmx_data.layers[0].data[192][154] = tmx_data.layers[1].data[192][154]
            level_Complete.play()
            end_S0 = 1
            
            

        if end_S0:
            button_Time -= 1
            if button_Time <= 0:
                C_H.health = health
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







        pygame.display.update()                         # Actually does the screen updated
        clock.tick(19)                                  # Run the game at 29 frames per second








#*****************************  Level_00  ************************************

width, height = 1420, 720                           # Set screen width,height (1420, 720)
pygame.init()                                       # Start graphics system
pygame.mixer.init()                                 # Start audio system
window = pygame.display.set_mode((width, height))   # Create window
pygame.display.set_caption("Baby Blue")
clock = pygame.time.Clock()                         # Create game clock

restart_Game = 1
i = 1
while(restart_Game == i):
    restart_Game = main()
    i = 0
    

pygame.quit()