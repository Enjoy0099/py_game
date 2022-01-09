import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame






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
    tmx_data = load_pygame("Final_map_End.tmx")




    pygame.mixer.music.load("sounds/intro_game_0.wav")
    pygame.mixer.music.play(1)
    jump_sfx = pygame.mixer.Sound("sounds/jump.wav")
    level_Complete = pygame.mixer.Sound("sounds/level_Complete.wav")
    game_over_wav = pygame.mixer.Sound("sounds/Game_Over.wav")




    Crash = pygame.image.load("imges/crash (1).png").convert_alpha()
    last_Img = pygame.image.load("imges/last (1).png").convert_alpha()
    Game_Over = pygame.image.load("imges/END (1).png").convert_alpha()




    y_ground = window.get_height() - 200
    x = 0
    y = y_ground
    world_offset = [-900,-4550]    #base :- (-900, -4500)

    end_S0 = 0
    button_Time = 19 * 2
    img_0 = 19 * 4
    img_1 = 19 * 4
    img_2 = 19 * 4
    over = 19 * 4

    quit = False
    can_not_move = 1




    stand = 0




    player_stand = pygame.image.load("assets/p1_stand.png").convert_alpha()
    player_stand = pygame.transform.scale(player_stand, (50,70))
    player_stand_left = pygame.transform.flip(player_stand, True, False)

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
    player_right_frame = 0  

    player_left = [pygame.transform.flip(image, True, False) for image in player_right]
    player_left_frame = 0

    player_jump = pygame.image.load("assets/p1_jump.png").convert_alpha()
    player_jump = pygame.transform.scale(player_jump, (50,70))
    player_jump_left = pygame.transform.flip(player_jump, True, False)
    player_jump_frame = 0

    player_land = pygame.image.load("assets/p1_duck.png").convert_alpha()
    player_land = pygame.transform.scale(player_land, (50,70))
    player_land_left = pygame.transform.flip(player_land, True, False)





    direction = "stand"
    



    while not quit:

        window.fill((247,190,192))  




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











        if standing_on_left["id"] == 256 or standing_on_right["id"] == 256:
            tmx_data.layers[0].data[192][160] = 0
            tmx_data.layers[0].data[192][160] = tmx_data.layers[1].data[192][160]
            level_Complete.play()
            end_S0 = 1
            
            

        if end_S0:
            button_Time -= 1
            if button_Time <= 0:
                img_0 -= 1
                can_not_move = 0
            if img_0 <= 0:
                window.blit(Crash, (0,0))
                img_1 -= 1
            if img_1 <= 0:
                window.blit(last_Img, (0,0))
                img_2 -= 1
            if img_2 <= 0:
                window.blit(Game_Over, (0,0))
                over -= 1
                if img_2 == -19:
                    game_over_wav.play()
            if over <= 0:
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







        pygame.display.update()                         # Actually does the screen updated
        clock.tick(19)                                  # Run the game at 29 frames per second








#*****************************  Level_00  ************************************

width, height = 1420, 720                           # Set screen width,height (1420, 720)
pygame.init()                                       # Start graphics system
pygame.mixer.init()                                 # Start audio system
window = pygame.display.set_mode((width, height))   # Create window
pygame.display.set_caption("Baby Blue")
clock = pygame.time.Clock()                         # Create game clock
main()
pygame.quit()