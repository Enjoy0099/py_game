
# ************************************************  Baby Blue *************************************************

import pygame, time, random
#from pygame import image
from pygame.locals import *

# library pytmx imported
from pytmx.util_pygame import load_pygame

# user define function
# task :- To render the map in pygame window
def blit_my_map(window, tmxdata, world_offset):

    # tile[0] -> x grid location
    # tile[1] -> y grid location
    # (x,y) -> position of the tile in the map
    # tile[2] -> image of the tile

    # render first layer and first layer index --> 0.
    for tile in tmxdata.layers[0].tiles():                       
        x_pixel = tile[0] * 35 + world_offset[0]                       
        y_pixel = tile[1] * 35 + world_offset[1]
        img = pygame.transform.scale(tile[2], (35,35))                        
        window.blit(img, (x_pixel, y_pixel) )
    
    # # render both layer.
    # for layer in tmxdata:
    #     for tile in layer.tiles():
                                   

def get_my_tiles_properties(tmxdata, x, y, world_offset):
    world_x = x - world_offset[0]  # particular tile
    world_y = y - world_offset[1]

    tile_x = world_x // 35
    tile_y = world_y // 35

    properties = tmxdata.get_tile_properties(tile_x, tile_y, 0)

    # If player is not moving in the map (moving in a free space)
    if properties is None:
        properties = {"id": -1, "climbable": False, "ground": False, "health": 0, "points": 0, 
                      "provide": "", "require": "", "solid": False}
        
    # position of the tile
    properties["x"] = tile_x
    properties["y"] = tile_y

    return properties


def main():

    #******************************************* Game variables ***********************************************************
    
    font = pygame.font.SysFont("font/Viga-Regular.ttf", 40)      # import font and apply size
    coin_img = pygame.image.load("imges/coin.png").convert_alpha()
    health_img = pygame.image.load("imges/hea.png").convert_alpha()

    world_offset = [-600,0]                  # which part of the map to show to the player
    tmx_data = load_pygame("my_map.tmx")
    stand = 0                                # player stand use in images
    health_wait = 0

    # this music is runing only once when game is start
    pygame.mixer.music.load("sounds/intro_game_0.wav")
    pygame.mixer.music.play(1)  # tell us to loop run once

    # coin, jump and injury is played conditionally
    coin_sfx = pygame.mixer.Sound("sounds/coin.wav")
    jump_sfx = pygame.mixer.Sound("sounds/jump.wav")
    injury_sfx = pygame.mixer.Sound("sounds/hurt_1.wav")
    key_sfx = pygame.mixer.Sound("sounds/key.wav")
    next_level = pygame.mixer.Sound("sounds/level_increased.wav")
    health_rise = pygame.mixer.Sound("sounds/health.wav")

    collected_items = []   # to check what player has collected

    y_ground = window.get_height() - 160
    
    quit = False
    x = 400
    y = y_ground

    health = 3 # full health of player
    points = 0

    #************ single image load and scale *****************
    player_stand = pygame.image.load("assets/p1_stand.png").convert_alpha()
    player_stand = pygame.transform.scale(player_stand, (50,70))
    player_stand_left = pygame.transform.flip(player_stand, True, False)

    #************** multiple image load and scale ***************
    player_right = [
        pygame.image.load("assets/p1_walk/PNG/p1_walk01.png").convert_alpha(),
        pygame.image.load("assets/p1_walk/PNG/p1_walk02.png").convert_alpha(),
        pygame.image.load("assets/p1_walk/PNG/p1_walk03.png").convert_alpha(),
        pygame.image.load("assets/p1_walk/PNG/p1_walk04.png").convert_alpha(),
        pygame.image.load("assets/p1_walk/PNG/p1_walk05.png").convert_alpha(),
        pygame.image.load("assets/p1_walk/PNG/p1_walk06.png").convert_alpha(),
        pygame.image.load("assets/p1_walk/PNG/p1_walk07.png").convert_alpha(),
        pygame.image.load("assets/p1_walk/PNG/p1_walk08.png").convert_alpha(),
        pygame.image.load("assets/p1_walk/PNG/p1_walk09.png").convert_alpha(),
        pygame.image.load("assets/p1_walk/PNG/p1_walk10.png").convert_alpha(),
        pygame.image.load("assets/p1_walk/PNG/p1_walk11.png").convert_alpha()
    ]
    player_right = [pygame.transform.scale(image, (50,70)) for image in player_right]
    player_right_frame = 0   # index tracker of the player_right list

    player_left = [pygame.transform.flip(image, True, False) for image in player_right]
    player_left_frame = 0

    player_jump = pygame.image.load("assets/p1_jump.png").convert_alpha()
    player_jump = pygame.transform.scale(player_jump, (50,70))
    player_jump_left = pygame.transform.flip(player_jump, True, False)
    player_jump_frame = 0

    

    player_land = pygame.image.load("assets/p1_duck.png").convert_alpha()
    player_land = pygame.transform.scale(player_land, (50,70))
    player_land_left = pygame.transform.flip(player_land, True, False)
    
    direction = "stand"   # current position of player image



    #********************************************** Start game loop ******************************************************
    while not quit:

        window.fill((207,237,238))                            # Reset screen to black

        #********** Process events **********

        blit_my_map(window, tmx_data, world_offset)

        coin_no = font.render(f"{points}", 1, (248,207,64))
        health_no = font.render(f"{health}", 1, (255,37,17))

        window.blit(health_img, (1, 0))
        window.blit(health_no, (40, 5))
        window.blit(coin_img, (-15, 19))
        window.blit(coin_no, (40, 44))
        


        keyspressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit = True
        
        # Important
        standing_on = get_my_tiles_properties(tmx_data, x + 25, y + 70, world_offset)
        # print(standing_on)

        #************ Move ******************
        if keyspressed[ord("a")]:
            stand = 1
            left_tile = get_my_tiles_properties(tmx_data, x - 10, y + 15, world_offset)
            left_tile_0 = get_my_tiles_properties(tmx_data, x - 10, y + 55, world_offset)
            if not left_tile["solid"] and not left_tile_0["solid"]:
                x = x - 10
                direction = "left"

        if keyspressed[ord("d")]:
            stand = 0
            right_tile = get_my_tiles_properties(tmx_data, x + 50 + 10, y + 15, world_offset)
            right_tile_0 = get_my_tiles_properties(tmx_data, x + 50 + 10, y + 55, world_offset)
            if not right_tile["solid"] and not right_tile_0["solid"]:
                x = x + 10
                direction = "right"

        if keyspressed[ord("w")]:
            above_tile = get_my_tiles_properties(tmx_data, x + 5, y - 10, world_offset)
            above_tile_0 = get_my_tiles_properties(tmx_data, x + 45, y - 10, world_offset)

            if standing_on["climbable"] == True:
                y = y - 10   # moving upward

            # player jump only when player is at ground
            if not above_tile["solid"] and not above_tile_0["solid"]:
                if standing_on["ground"] == True:

                    jump_sfx.play()

                    player_jump_frame = 10      # Power of jump
                    # y = y - 10
                    # direction = "jump"
        
            else:
                player_jump_frame = 0


        above_tile_left = get_my_tiles_properties(tmx_data, x + 25 - 15, y - 10, world_offset)
        above_tile_right = get_my_tiles_properties(tmx_data, x + 25 + 15, y - 10, world_offset)
        if above_tile_right["solid"] or above_tile_left["solid"]:
            player_jump_frame = 0


        if keyspressed[ord("s")]:
            if standing_on["climbable"]:
                y = y + 10

            # y = y + 10
            # direction = "landing"

        if sum(keyspressed) == 0:        # checking if no key pressed from keyboard
            direction = "stand"

        if standing_on["health"] < 0 and health_wait == 0:
            health = health + standing_on["health"] # health decrease
            health_wait = 19                        # FPS of Game
        if health_wait != 0:
            health_wait -= 1
        if standing_on["health"] < 0:
            injury_sfx.play()

        if health < 0:
            quit = True

        # touching heart
        touching_heart = get_my_tiles_properties(tmx_data, x + 44, y + 15, world_offset)
        touching_heart_left = get_my_tiles_properties(tmx_data, x + 6, y + 15, world_offset)

        #touching heart icon then increase health
        if touching_heart["id"] == 466:
            health = health + touching_heart["health"]
            health_rise.play()
            tmx_data.layers[0].data[touching_heart["y"]][touching_heart["x"]] = 0

        elif touching_heart_left["id"] == 466:
            health = health + touching_heart_left["health"]
            health_rise.play()
            tmx_data.layers[0].data[touching_heart_left["y"]][touching_heart_left["x"]] = 0

        # collision handling
        touching_coins = get_my_tiles_properties(tmx_data, x + 44, y + 15, world_offset)
        touching_coins_left = get_my_tiles_properties(tmx_data, x + 6, y + 15, world_offset)

        # touching the coin
        if touching_coins["id"] == 288:
            tile_x = touching_coins["x"]
            tile_y = touching_coins["y"]
            coin_sfx.play()
            points = points + touching_coins["points"]
            # above the position of touched coin
            tmx_data.layers[0].data[tile_y][tile_x] = 0  # to remove coin after it is collected

        elif touching_coins_left["id"] == 288:
            tile_x_left = touching_coins_left["x"]
            tile_y_left = touching_coins_left["y"]  
            coin_sfx.play()
            points = points + touching_coins_left["points"]
            # above the position of touched coin
            tmx_data.layers[0].data[tile_y_left][tile_x_left] = 0


        # for lock and keys achievements

        touching_locks_keys = touching_coins
        touching_locks_keys_leftside = touching_coins_left

        if touching_locks_keys["provide"] != "" :
            if touching_locks_keys["provide"] == "green key":
                collected_items.append(touching_locks_keys["provide"])
                key_sfx.play()
                tmx_data.layers[0].data[touching_locks_keys["y"]][touching_locks_keys["x"]] = 0

        elif touching_locks_keys_leftside["provide"] != "" :
            if touching_locks_keys_leftside["provide"] == "green key":
                collected_items.append(touching_locks_keys_leftside["provide"])
                key_sfx.play()
                tmx_data.layers[0].data[touching_locks_keys_leftside["y"]][touching_locks_keys_leftside["x"]] = 0

        # green lock is touched by player
        if touching_locks_keys["require"] in collected_items or touching_locks_keys_leftside["require"] in collected_items:

            # unlock of the door
            item = touching_locks_keys["require"]
            item_0 = touching_locks_keys_leftside["require"]

            if item == "green key" or item_0 == "green key":
                
                # finally unlock the door
                # override the door from tile layer 2 into tile layer 1

                tmx_data.layers[0].data[touching_locks_keys["y"]][touching_locks_keys["x"]] = 0
                tmx_data.layers[0].data[touching_locks_keys_leftside["y"]][touching_locks_keys_leftside["x"]] = 0

                tmx_data.layers[0].data[44][66] = tmx_data.layers[1].data[44][66]
                tmx_data.layers[0].data[45][66] = tmx_data.layers[1].data[45][66]

                next_level.play()

        
        # Checking whether there is jump
        # Progress on jumping
        if player_jump_frame > 0:
            y = y - 10
            direction = "jump"
            player_jump_frame = player_jump_frame - 1

        #Progress on falling/landing
        elif standing_on["ground"] == False and standing_on["climbable"] == False:          # Gravity applied
            y = y + 10
            direction = "landing"



        #**************** Bounded ****************
        if x < 360:
            x = 360
            world_offset[0] += 10

        if x > window.get_width() - 360 - 25:
            x = window.get_width() - 360 - 25
            world_offset[0] -= 10

        if y < 140:
            y = 140
            world_offset[1] += 10

        if y > y_ground:
            y = y_ground
            world_offset[1] -= 10



        #**************************************************** Your game logic here *****************************************
        # player = Rect(x, y, 44, 44)
        # pygame.draw.rect(window, (67,176,241), player)

        # Draw the player based on direction variable

        if direction == "left":
            window.blit(player_left[player_left_frame], (x,y))
            player_left_frame = (player_left_frame + 1) % len(player_right)
            
        elif direction == "right":
            window.blit(player_right[player_right_frame], (x,y))
            player_right_frame = (player_right_frame + 1) % len(player_right)
                # if (player_right_frame >= len(player_right)):
                #   player_right_frame = 0
        
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


        #********** Update screen **********
        pygame.display.update()                         # Actually does the screen updated
        clock.tick(19)                                  # Run the game at 19 frames per second



#************************************************* Initialise & run the game **********************************************
if __name__ == "__main__":
    width, height = 1420, 720                           # Set screen width,height (1420, 720)
    pygame.init()                                       # Start graphics system
    pygame.mixer.init()                                 # Start audio system
    window = pygame.display.set_mode((width, height))   # Create window
    pygame.display.set_caption("Baby Blue")
    clock = pygame.time.Clock()                         # Create game clock
    main()
    pygame.quit()