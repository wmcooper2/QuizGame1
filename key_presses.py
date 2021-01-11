#std lib
from typing import Any

#3rd party

#custom
from constants import constants as c
import items as i
import util as u

def handle_key_presses(yammy: Any) -> None:

    #disappear Yammy
    if u.key_f():
        yammy.toggle_disappear()

    #Transfer item to player 1
    elif u.key_1() and not u.any_movement(c.PLAYERS, c.ALL_ITEMS) and not u.black_box_visible():
        yammy.wave_wand()
        c.P1.inventory = u.remove_item_from_all_items()
        i.add_item()
        print("all items:", c.ALL_ITEMS)
        print("p1 item:", c.P1.inventory)

    elif u.key_left() and not u.movement(c.PLAYERS) and not u.black_box_visible():
        u.rotate_players_left()

    elif u.key_right() and not u.movement(c.PLAYERS) and not u.black_box_visible():
        u.rotate_players_right()

    elif u.key_up() and not u.movement(c.PLAYERS) and not u.black_box_visible():
        c.PLAYERS = u.mix(c.PLAYERS)

    #plus one point
#     elif u.key_o() and u.player1_has_item():
    elif u.key_o() and u.player1_has_item() and not u.movement(c.PLAYERS):
#         print("has item?", u.player1_has_item())
        u.right_answer(c.P1)
        u.rotate_players_left()


    #minus one point
    elif u.key_x() and u.player1_has_item() and not u.movement(c.PLAYERS):
        u.wrong_answer(c.P1)
        u.rotate_players_left()
        #TODO, delete player's inventory
        if c.P1.inventory:
            c.P1.inventory.delete()

    elif u.key_a() and not u.movement(c.ALL_ITEMS):
        pass
        u.rotate_items_left()

    elif u.key_d()  and not u.movement(c.ALL_ITEMS):
        pass
        u.rotate_items_right()

    elif u.key_s() and not u.movement(c.ALL_ITEMS):
        pass
        c.ALL_ITEMS = u.mix(c.ALL_ITEMS)
