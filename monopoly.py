# -*- coding: utf-8 -*-
"""Monopoly.ipynb

Original file is located at
    https://colab.research.google.com/drive/1SrRSLQ2Dl_CPaHuyUnC_xCeEWmKLHSgw
"""

import random
from IPython.core.display import Image, display
from ipythonblocks import BlockGrid, colors
from PIL import Image as image

"""# Set up simulation

1. `roll_dice` simulates rolling a pair of dice; returns the value rolled
2. `chance` selects a Chance card with uniform probability based on the quantities of cards in the deck
3. `take_turn` takes as input the current position on the board. It rolls the dice then returns the position on the board after moving.
4. `go_to_jail` returns the board position of the jail square
5. `draw_chance` takes as input the current position on the board. It draws a Chance card then returns the position on the board after following the instructions.
6. `play_game` simulates 100 turns by a player and returns a "game board" which is a list with one element for each square on a Monopoly board. `board[i]` contains the number of times that the player landed on square i.

## See below for visualization of results!
"""

def roll_dice():
    
    # Roll a die
    d1 = random.randrange(1,7)
    
    # Roll the other die
    d2 = random.randrange(1,7)
    
    # If you roll doubles, roll again
    if d1==d2:
        return d1 + d2 + roll_dice()
    
    return d1+d2

# Select a Chance card
def chance():
    chance_cards_dict = {
        'jail_free': 1,
        'collect_money': 3,
        'pay_money': 3,
        'go_to_jail':1
    }
    chance_cards=[]
    for card in chance_cards_dict:
        for i in range(0, chance_cards_dict[card]):
            chance_cards.append(card)
    
    advance_cards = ['nearest_utility', 'three_back', 'nearest_railroad','go','st_charles','illinois','boardwalk','reading_rr']
    chance_cards.extend(advance_cards)
    return random.choice(chance_cards)

board_squares = 40
def take_turn(position):
    return (position + roll_dice()) % board_squares

# ASSUMPTION: if you roll doubles, you do not take the action on the square landed on; you just move to that square then roll again
# ASSUMPTION: if you go to jail, you pay the bail and exit on your next turn

jail = 10
go = 0
reading_rr = 5
pennsylvania_rr = 15
bo_rr = 25
shortline_rr = 35
mediterranean = 1
boardwalk = 39
chance1 = 8
chance2 = 22
chance3 = 36
electric = 12
waterworks = 28
st_charles = 11
illinois = 24
go_to_jail = 30


def go_to_jail():
    return jail

def draw_chance(position):      
        
    if position not in [chance1, chance2, chance3]:
        print('error!!')
        
    card = chance()
        
    if card == 'nearest_utility':
        if position == chance1 or position == chance3:
            return electric
        else:
            return waterworks
        
    if card == 'three_back':
        return position - 3
    
    if card == 'nearest_railroad':
        if position == chance1:
            return pennsylvania_rr
        if position == chance2:
            return bo_rr
        else:
            return reading_rr
        
    if card == 'go':
        return go
    
    if card == 'st_charles':
        return st_charles
    
    if card == 'illinois':
        return illinois
    
    if card == 'boardwalk':
        return boardwalk
    
    if card == 'reading_rr':
        return reading_rr
    
    if card == 'go_to_jail':
        return jail
    
    # Else it's not a movement card
    return position
    
def play_game():
    position = 0
    board = [0] * board_squares

    # Take 100 turns
    for i in range(0,100):

        # First, roll the dice
        position = take_turn(position)
        
        # Make note that the space was landed on
        board[position] += 1
        
        # Did you land on Chance?
        if position in [chance1, chance2, chance3]:
            new_position = draw_chance(position)
            
            # If the Chance card moved you, make note of the new space you landed on
            if new_position != position:
                position = new_position
                board[position] += 1
        
        # Did you land on Go to Jail?
        if position == go_to_jail:
            position = go_to_jail()
            board[position] += 1
            
    return board

"""# Now we run 1000 "games" and visualize the results.

The darker the square, the more it's landed on.
"""

average_landings = [0] * board_squares

for i in range(0, 1000):
    board = play_game()
    average_landings = [avg + (new/100.0) for avg, new in zip(average_landings, board)]

average_landings = [avg/10.0 for avg in average_landings]
print('Probability (%) of landing on...')
print('Reading Railroad:\t', average_landings[reading_rr])
print('Pennsylvania Railroad:\t', average_landings[pennsylvania_rr])
print('B. & O. Railroad:\t', average_landings[bo_rr])
print('Short Line Railroad:\t', average_landings[shortline_rr])
print('GO:\t\t\t', average_landings[go])
print('Mediterranean Avenue:\t', average_landings[mediterranean])
print('Boardwalk:\t\t', average_landings[boardwalk])

width = 11
height = 11
grid = BlockGrid(width=width, height=height,
                     fill=(209, 194, 111))

# Set up palette
tups = [(elt, p) for elt, p in zip(range(0, board_squares), average_landings)]
tups.sort(key = lambda x: x[1], reverse = True)
ranks = [(rank, elt[0], elt[1]) for rank, elt in zip(range(0, board_squares), tups)]
palette = [0] * board_squares
for i in range(0, board_squares):
    idx = ranks[i][1]
    palette[idx] = ranks[i][0] * 6.25
    
# Paint edges
# Top row
for i in range(0, width):
    colour = palette[20 + i]
    grid[0, i] = (colour, colour, colour)
    
# Bottom row
for i in range(0, width):
    colour = palette[10-i]
    grid[height - 1, i] = (colour, colour, colour)

# Left side
for i in range (0, height):
    colour = palette[20 - i]
    grid[i, 0] = (colour, colour, colour)
    
# Right side
for i in range (0, height-1):
    colour = palette[30 + i]
    grid[i, width - 1] = (colour, colour, colour)
    

grid.show()