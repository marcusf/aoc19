import utils
from collections import defaultdict, namedtuple
from math import floor, ceil, copysign, sin, cos, radians, degrees

scale, traces = 3, 1440
width, height = 0, 0

def big(v): return ceil(scale*v+scale/2)-1
def small(v): return floor((v-scale/2)/scale)+1

def get_input():
    global width, height

    mp = utils.read_input_multi(delim_2=None, fname='10.input', generator=str)

    width, height = scale*len(mp[0]), scale*len(mp)

    grid = [[0 for _ in range(width)] for _ in range(height)]

    i = 0
    for y, row in enumerate(mp):
        for x, coord in enumerate(row):
            if coord == '#':
                i+=1
                grid[big(y)][big(x)] = 1

    return grid 

def scan_one(grid, x, y):
    trace_span = radians(360 / traces)
    hits = set()
    ox, oy = x, y
    for phi in range(traces):
        dx = cos(phi*trace_span)
        dy = sin(phi*trace_span)

        x, y = ox, oy
        while x >= 0 and round(x) < width and y >= 0 and round(y) < height:
                
            if grid[round(y)][round(x)] == 1 and not (x == ox and y == oy):
                #print(f'Found a hit from ({small(ox)}, {small(oy)}) at ({small(x)},{small(y)}) with angle {round(degrees(phi*trace_span))}')
                hits.add((round(x),round(y)))
                break
            x += dx
            y += dy
    return hits

def print_grid(grid):
    for row in grid:
        print(''.join(['#' if x == 1 else '.' for x in row]))

grid = get_input()
print_grid(grid)
output = {}
for y, row in enumerate(grid):
    for x, val in enumerate(row):
        if val == 1:
            output[small(x), small(y)] = len(scan_one(grid, x, y))

#print(output)

maxpos, maxval = 0, 0
for k, v in output.items():
    if v > maxval:
        maxpos = k
        maxval = v

print(maxpos, maxval)