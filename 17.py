from utils import *
from interp import *
from compress import compress
import re

def mk_grid(output):
    m = GridLayer(str)
    for y, row in enumerate(''.join([chr(o) for o in output]).split("\n")):
        for x, ch in enumerate(row):
            m[(x,y)] = ch
    
    return m

def part1():
    ip = interpreter(read_input())
    output, _ = ip.run_until_blocked() 
    m = mk_grid(output)
    alignments = []

    for c in list(m.grid.keys()):
        item = m[c]
        if item == '#':
            if m[c+(-1,0)] == '#' and m[c+(1,0)] == '#'\
                and m[c+(0,1)] == '#' and m[c+(0,-1)] == '#':
                alignments.append((c.x,c.y))

    print(sum([x*y for (x,y) in alignments]))

#part1()

def get_start(m):
    for k,v in m.grid.items():
        if v == '^':
            return k

VISITED = 1
NOT_VISITED = 0

def get_path_recursive(grid, pos, dr, path_so_far, passed_xs, paths, d=0):
    
    while True:

        if pos in path_so_far and grid[pos] == '#':
            return

        path_so_far.append(pos)

        if grid[pos+dr] == '#' or pos+dr in passed_xs:
            pos = pos + dr
            continue
        elif grid[pos+dr] == '+' and not (pos+dr in passed_xs):
            p = pos
            pos = pos+dr
            passed_xs.append(pos)
            for pos2, ch, _ in grid.adjacent(pos):
                if not pos2 in path_so_far and ch == '#':
                    dr = pos2-pos
                    get_path_recursive(grid, pos, Coord2D(dr.x, dr.y), path_so_far[:], passed_xs[:], paths, d+1)
        else:
            dr.rotate90()
            if grid[pos+dr] == '#':
                pos = pos + dr
            else:
                dr.rotate90()
                dr.rotate90()
                if grid[pos+dr] == '#':
                    pos = pos + dr
                else:
                    paths.add(tuple(path_so_far))
                    return
    

def get_path(grid):
    pos = get_start(grid)
    paths = set()
    print(sum([1 for g in grid.grid.values() if g == '#']))

    dr = Coord2D(1,0)
    steps = []
    while True:
        steps.append(pos)
        if grid[pos+dr] == '#':
            pos = pos + dr
            continue
        else:
            dr.rotate90()
            if grid[pos+dr] == '#':
                pos = pos + dr
            else:
                dr.rotate90()
                dr.rotate90()
                if grid[pos+dr] == '#':
                    pos = pos + dr
                else:
                    break

    direction = Coord2D(-1,0)
    i = 0
    ll = ['R']
    for cur, next in zip(steps,steps[1:]):
        if cur-next == direction:
            i = i + 1
        else:
            ll.append(str(i))
            i = 1
            
            if (cur-next) == direction.rotate90():
                ll.append('R')
            elif (cur-next) == direction.rotate90().rotate90():
                ll.append('L')
            

    ll.append(str(i))
    
    return steps, ll


def part2():
    ip = interpreter(read_input())
    ip.code[0] = 2
    output, _ = ip.run_until_blocked()
    grid = mk_grid(output)
    _, instr = get_path(grid)

    ss = ','.join([a+str(b) for a,b in chunk(instr,2)])
    opt = compress(ss.split(','))

    ip.input = [ord(c) for c in opt[0]]
    output, _ = ip.run_until_blocked()    

    ip.input = [ord(c) for c in opt[1]]
    output, _ = ip.run_until_blocked()

    ip.input = [ord(c) for c in opt[2]]
    output, _ = ip.run_until_blocked()

    ip.input = [ord(c) for c in opt[3]]
    output, _ = ip.run_until_blocked()

    ip.input = [ord(c) for c in 'n\n']
    output, _ = ip.run_until_blocked()

    print(output[-1])



part2()
