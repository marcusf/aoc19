# In which Marcus learns to implement a proper BFS
# courtesy of https://github.com/krka/adventofcode2019/blob/master/src/main/java/aoc/Day18.java
from utils import *
from math import ceil
from copy import deepcopy
import heapq
from collections import namedtuple

def get_map(fname):
    starts = []
    input = read_input('\n', generator=str, fname=fname)
    mp = GridLayer(str)
    keys, doors = dict(), dict()

    for y, row in enumerate(input):
        for x, v in enumerate(row):
            if v == '@':
                starts.append(Coord2D(x,y))
            else:
                mp[(x,y)] = v
            if v.islower():
                keys[v] = Coord2D(x,y)
            elif v.isupper():
                doors[v] = Coord2D(x,y)
    return mp, starts, keys, doors

class state(namedtuple('state','pos keys steps')):
    __slots__ = ()
    def __eq__(self,other):
        return self.pos == other.pos and self.keys == other.keys
    def __hash__(self):
        return hash((self.pos, self.keys))

def update(mapp, doors, keys, current, dp, target):
    new_pos = current.pos + dp
    if mapp[new_pos] == '#':
        return None
    elif new_pos in doors:
        if not mapp[new_pos].lower() in target:
            return state(new_pos, current.keys, current.steps+1)
        elif mapp[new_pos].lower() in current.keys:
            return state(new_pos, current.keys, current.steps+1)
        else:
            return None
    elif new_pos in keys:
        return state(new_pos, frozenset(current.keys | {mapp[new_pos]}), current.steps+1)
    else:
        return state(new_pos, current.keys, current.steps+1)

def bfs(m, d, k, start, target):
    queue = []
    visited = set()
    queue.append(state(start, frozenset(), 0))
    visited.add(start)
    while queue:
        curr = queue.pop(0)
        if curr.keys == target:
            return curr.steps

        for dp in [(-1,0),(1,0),(0,-1),(0,1)]:
            new_state = update(m, d, k, curr, dp, target)
            if new_state and not new_state in visited:
                visited.add(new_state)
                queue.append(new_state)

def part1():
    mapp, starts, keys, doors = get_map('18.input')
    doorst = set(doors.values())
    keyst = set(keys.values())
    print(bfs(mapp, doorst, keyst, starts[0], frozenset(keys.keys())))

def part2():
    mapp, starts, keys, doors = get_map('18b.input')
    doorst = set(doors.values())
    keyst = set(keys.values())

    _, _, w, h = mapp.bounds()
    buckets = [set(),set(),set(),set()]
    for k, v in keys.items():
        x, y = v
        ww = w//2
        hh = h//2
        p = 0 if x < ww and y < hh else 1 if x >= ww and y < hh else 2 if x < ww and y >= hh else 3
        buckets[p].add(k)

    print(sum([bfs(mapp, doorst, keyst, starts[i], frozenset(buckets[i])) for i in range(4)]))

part1()
part2()