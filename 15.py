from utils import *
from interp import *
import sys
from random import randint
from getch import getch
from collections import defaultdict

BLOCKED = 0
MOVED_ONCE = 1
FOUND = 2

VISITED=1
NOT_VISITED=0

EMPTY = 1
WALL = 2
CHARACTER = 3
OXYGEN = 4
ORIGO = 5

def printer(c): 
    return [' ','.','#','X','O','S'][c]

pos = Coord2D(0,0)
move = Coord2D(0,-1)
mapp = GridLayer()
oxygen = Coord2D(0,0)
trails, path = list(), list() #defaultdict(list)
backtrack = False

def coord_ret(coord):
    if coord == (-1,0): return 1
    if coord == (1,0):  return 2
    if coord == (0,-1): return 3
    if coord == (0,1):  return 4 

def reverse(coord):
    if coord == (-1,0): return Coord2D(1,0)
    if coord == (1,0):  return Coord2D(-1,0)
    if coord == (0,-1): return Coord2D(0,1)
    if coord == (0,1):  return Coord2D(0,-1)

# Only four movement commands are understood: 
# north (1), south (2), west (3), and east (4).
# The repair droid can reply with any of the following status codes:
#
# 0: The repair droid hit a wall. Its position has not changed.
# 1: The repair droid has moved one step in the requested direction.
# 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
def navigate(inp):
    global pos, move, mapp, trails, backtrack, path, oxygen

    assert(len(inp) == 1)
    response = inp[0]
    
    mapp[(0,0)] = ORIGO

    mapp.put_meta(pos, VISITED)
    mapp.put_meta(pos+move, VISITED)

    if response == FOUND:
        mapp[pos+move] = OXYGEN
        oxygen = pos+move
        print(f'(A) Total moves: {len(path)+1}')

    if response == BLOCKED:
        mapp[pos+move] = WALL
    elif response == MOVED_ONCE or response == FOUND:
        if not backtrack:
            trails.append(reverse(move))
            path.append(pos+move)
        if mapp[pos] != OXYGEN:
            mapp[pos] = EMPTY
        pos += move
        if mapp[pos] != OXYGEN:
            mapp[pos] = CHARACTER        
    
    
    if mapp.get_meta(pos+move) != VISITED and mapp[pos+move] != WALL:
        backtrack = False
    elif mapp.get_meta(pos+move.rotate90()) != VISITED and mapp[pos+move] != WALL:
        backtrack = False
    elif mapp.get_meta(pos+move.rotate90().rotate90()) != VISITED and mapp[pos+move] != WALL:
        backtrack = False
    elif mapp.get_meta(pos+move.rotate270()) != VISITED and mapp[pos+move] != WALL:
        backtrack = False
    else:
        backtrack = True
        if len(trails) == 0:
            return [], False
        else:
            move = trails.pop()
            path.pop()

    return [coord_ret(move)], True

def flood_fill(mapp, start_pos):
    ticks = 0
    posses, ps = [start_pos], []
    while True:
        for pos in posses:
            if mapp[pos+(0,1)] == EMPTY:
                mapp[pos+(0,1)] = OXYGEN
                ps.append(pos+(0,1))
            if mapp[pos+(0,-1)] == EMPTY:
                mapp[pos+(0,-1)] = OXYGEN
                ps.append(pos+(0,-1))
            if mapp[pos+(1,0)] == EMPTY:
                mapp[pos+(1,0)] = OXYGEN
                ps.append(pos+(1,0))
            if mapp[pos+(-1,0)] == EMPTY:
                mapp[pos+(-1,0)] = OXYGEN
                ps.append(pos+(-1,0))

        if len(ps) == 0:
            print(f'(B) {ticks} to flood fill')
            return
        ticks+=1
        posses = ps
        ps = []

icp = interpreter(read_input())
icp.input.append(1)
icp.run(navigate)
flood_fill(mapp, oxygen)