#std lib
from pprint import pprint
import random

#3rd party
import pyglet

#custom
from animations import transfer_item
from constants import Constants as c
from draw_loop import draw_menu, draw_problem, draw_sprites
import items as i
from key_presses import handle_key_presses
import util as u
import sprites as s

#TODO, add the star, feather and question block to the game

#NOTE, the business logic is separated from the drawing of the sprites in the update loops

#Music
# source = pyglet.media.load('explosion.wav')
# source = pyglet.resource.media('overworld.mp3')
source = pyglet.media.load('./music/overworld.mp3')
source.play()


#SPRITES
background = c.SPRITE(c.IMG("grassland.png"), batch=c.BACKGROUND_BATCH)
yammy = s.Yammy()

#floaters
fire_light = s.FireLight()
big_boo = s.BigBoo()

#walkers
dragon = s.Dragon()
green_koopa = s.GreenKoopa()
big_mole = s.BigMole()
mario = s.Mario()
luigi = s.Luigi()


#PLAYERS
c.ALL_PLAYERS = [
    mario,
    luigi,
    fire_light,
    dragon,
    big_boo,
    green_koopa,
    big_mole]


c.WALKING_PLAYERS = [
    dragon,
    green_koopa,
    big_mole,
    mario,
    luigi]

c.FLOATING_PLAYERS = [
    fire_light,
    big_boo]

#SOME SETUP
#Items
u.set_item_spots()
i.add_items()

#Players
u.set_player_spots()
u.add_players()

#Scores
#TODO, move these to their respective classes?
u.set_score_spots()
u.set_score_indices()
u.set_player_score_sprites()
u.assign_x_pos_to_player_score_sprites()
u.set_score_values_x()

question = c.NEW_QUESTION
problem = s.Problem()

def update_items(dt) -> None:
    for item in c.ALL_ITEMS:
        item.dest_x = c.ITEM_SPOTS[c.ALL_ITEMS.index(item)]
        item.update(dt)
    if c.TRANSFER_ITEM is not None:
        c.TRANSFER_ITEM.update(dt)
    
def update_players(dt) -> None:
    #update player positions
    for p in c.PLAYERS:
        p.spot = c.PLAYER_SPOTS[c.PLAYERS.index(p)]
        p.update(dt)

def update(dt) -> None:
    """This handles the business logic."""
    yammy.update()
    update_players(dt)
    update_items(dt)
    handle_key_presses(yammy, problem)
    transfer_item()

    #update problem
#     if not u.black_box_visible():
#     if problem.showing:
#         problem.toggle()
#         problem.random_question()

@c.GAME_WINDOW.event
def on_draw() -> None:
    """This handles the drawing of the sprites on screen."""
    #TODO, make menu selection screen 
#     if c.MENU_SCREEN:
#         draw_menu()        
#     else:
    draw_sprites()
    if problem.showing:
        draw_problem(problem)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, c.FRAME_SPEED)
    pyglet.app.run()
