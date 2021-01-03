#std lib
import random

#3rd party
import pyglet

#custom
from constants import constants as c
import util as u
import players as sprites #TODO, change file name to sprites
import problems
import items #must come after sprites (resource mod is defined in sprites... move to main?) #not needed?
from playerscores import scores_setup
from itemsetup import new_item # must stay here... strange error

#SPRITES
background = sprites.Background(img=sprites.Background.background_img, batch=c.MAIN_BATCH)
yammy = sprites.make_yammy()
mario = sprites.make_mario()
luigi = sprites.make_luigi()
fire_light = sprites.make_firelight()
dragon = sprites.make_dragon()
big_boo = sprites.make_big_boo()
green_koopa = sprites.make_green_koopa()
big_mole = sprites.make_big_mole()

c.ALL_PLAYERS = [
    mario,
    luigi,
    fire_light,
    dragon,
    big_boo,
    green_koopa,
    big_mole]

#TODO, make a way to check if player is walking type so that I don't have to waste memory or complicate things by adding another list here for walking vs floating players.
c.WALKING_PLAYERS = [
    dragon,
    green_koopa,
    big_mole,
    mario,
    luigi]

c.FLOATING_PLAYERS = [
    fire_light,
    big_boo]

#local constants
PLAYER_SPOTS = u.Line.player_spots
ITEM_SPOTS = u.Line.item_spots
PROB = problems.Problem
BB = PROB.BLACK_BOX

#line setups
lines = u.Line(screen_w=c.SCREEN_W, num_players=c.NUM_PLAYERS, num_items=c.NUM_ITEMS)
lines.line_up()                         #player line up
lines.item_line_up(c.ALL_ITEMS)         #item line up
lines.top_row_line_up()                 #for scores and item at top of game_window
player_spots = lines.player_spots       #at players platform
item_spots = lines.item_spots           #at item platform
score_spots = lines.score_spots         #at top of game_window
inventory_spot = lines.inventory_spot   #at top center of game_window

#TODO, refactor the arg out
u.add_items(new_item)                     #sets up c.ALL_ITEMS
u.add_players(c.RANDOMIZE_PLAYERS)        #sets up c.PLAYERS
scores_setup(score_spots)               #sets up scores at top of screen

#Set Player 1, the player closest to the items
c.P1 = c.PLAYERS[0]

def update(dt) -> None:
    """Game update loop.
        Updates occur in this order;
            Item effects
            Yammy
            All players' x_pos
            Floating players y_pos
            c.ALL_ITEMS x_pos and y_pos
            c.ITEM x_pos and y_pos
    """

    #EFFECTS
#     if c.BOMBOMB_EFFECT:                                        #mix items
#         mix_items()
#         c.BOMBOMB_EFFECT = False                            #reset flag
#         u.item_clean_up()
#     if c.POW_BUTTON_EFFECT:                                 #all, minus one point
#         for player in c.PLAYERS:
#             player.points -= 1
#         c.POW_BUTTON_EFFECT = False                         #reset flag
#         u.item_clean_up()
# 
#    if constants.FEATHER_EFFECT:
#        print("change feather effect to something more interesting.")
#        u.rotate_players_left()
#        FEATHER_EFFECT = False                                 #reset flag
#        u.item_clean_up()
#    if constants.STAR_EFFECT:
#        print("change star effect to something more interesting.")
#        STAR_EFFECT = False                                    #reset flag
#        u.item_clean_up()
#    if constants.QUESTION_BLOCK_EFFECT:
#        print("change star effect to something more interesting.")
#        QUESTION_BLOCK_EFFECT = False                          #reset flag
#        u.item_clean_up()


    #YAMMY
    yammy.update()

    #ALL PLAYERS
    c.P1 = c.PLAYERS[0]     #reset player 1

    #update player positions
    for player in c.PLAYERS:
        player.spot = PLAYER_SPOTS[c.PLAYERS.index(player)]
        player.update(dt)

        #player automatically uses item
#         if player.inventory and c.SHOWING_BLACK_BOX == False: 
#             print("INVENTORY:", c.P1.inventory)
#             main_item = c.P1.inventory[0]
#             player.use_item() 
   
        #update player scores 
#         score_points = c.SCORE_DISPLAY[player.point_index].points #the integer value
#         score_object = c.SCORE_DISPLAY[player.point_index]        #the score object
#         if player.points != score_points: 
#             score_object.update(score_object, player)           #player_score is in a different instance than player

    #FLOATING PLAYERS
    #update floating players y_pos
    for player in c.FLOATING_PLAYERS:
        player.float()

    #ITEMS
    #update items x_pos and y_pos
    for item in c.ALL_ITEMS:
        item.dest_x = ITEM_SPOTS[c.ALL_ITEMS.index(item)]
        item.update(dt)

    if c.ITEM is not None:
        c.ITEM.update(dt)

    #KEY HANDLERS
    #disappear Yammy
    if u.key_f():
        yammy.toggle_disappear()

    #Transfer item to player 1
    elif u.key_1() and not u.any_movement() and not c.SHOWING_BLACK_BOX:
        yammy.wave_wand()
        temp = u.remove_item_from_all_items()
        temp.transfer_item()

        #TODO, remove parameter
        u.add_item(new_item)

    elif u.key_left() and not u.player_movement() and not c.SHOWING_BLACK_BOX:
        u.rotate_players_left()

    elif u.key_right() and not u.player_movement() and not c.SHOWING_BLACK_BOX:
        u.rotate_players_right()

    elif u.key_up() and not u.player_movement() and not c.SHOWING_BLACK_BOX:
        u.mix_players()

    #plus one point
    #TODO, figure out how to give the item to the player, and persist in their inventory
    elif u.key_o() and u.player1_has_item():
        u.right_answer(c.P1)
        u.item_clean_up()

    #minus one point
    elif u.key_x() and u.player1_has_item():
        u.wrong_answer(c.P1)
        u.item_clean_up()

    elif u.key_a() and not u.item_movement():
        u.rotate_items_left()

    elif u.key_d()  and not u.item_movement():
        u.rotate_items_right()

    elif u.key_s() and not u.item_movement():
        u.mix_items()

#TODO, rotate players after certain key presses, but not all

@c.GAME_WINDOW.event
def on_draw() -> None:
    """Draw the visual elements."""
    c.GAME_WINDOW.clear()
    c.MAIN_BATCH.draw()
    c.P1 = c.PLAYERS[0]

#     if c.P1.has_item():
    #if c.P1's inventory has anything, it returns True
    if c.P1.inventory:
        # basic pattern:
            # draw the black box
            # change the guide
            # change the question in the problem
            # draw the guide
            # draw the question        
#         main_item = c.P1.inventory[0]
        main_item = c.P1.inventory
#         BB.draw()
#         S_BB = True     #set flag

        if c.NEW_QUESTION:
            c.NEW_QUESTION = False    #reset flag
            #simple vocab
            if isinstance(main_item, RedMushroom):    
                PROB.random_english_word()
            #verbs
            elif isinstance(main_item, GreenMushroom):  
                PROB.random_present_verb()
            #Japanese to English translation
            elif isinstance(main_item, PirahnaPlant):   
                PROB.random_target_sentence()
            #pronunciation
            elif isinstance(main_item, YoshiCoin):      
                PROB.random_pronunciation()
            #answer the question
            elif isinstance(main_item, SpinyBeetle):    
                PROB.random_question()
#         PROB.guide.draw()
#         PROB.question.draw()

    #top row scores
    for score in c.SCORE_DISPLAY:
        if score.points == 0:
            score.zero.draw()
        elif abs(score.points) > 0 and abs(score.points) <= 5:
            for element in score.small_score:
                element.draw()
        elif abs(score.points) > 5:
            for element in score.big_score:
                element.draw()


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, c.FRAME_SPEED)
    pyglet.app.run()
