from collections import defaultdict
import utils

pp = utils.read_input_multi(fname='03.input')
grid = utils.Grid()

dir = {'R':(1,0),'L':(-1,0),'U':(0,1),'D':(0,-1)}

def parse_instruction(instr, layer, pos, cost):
    x, y = pos
    dist = int(instr[1:])
    dx, dy = dir[instr[0]]
    for d in range(0,dist):
        layer[(x+dx*d,y+dy*d)] = 1
        layer.putif_meta(x+dx*d, y+dy*d, 0, cost+d)
    return((x+dx*dist,y+dy*dist), cost+dist)

for i, line in enumerate(pp):
    pos, cost = (0,0), 0
    layer = grid.add_layer()
    for item in line: pos, cost = parse_instruction(item, layer, pos, cost)

mindist, mincost = 9999999999999, 9999999999999

for cord in grid.intersection():
    if cord != (0,0):
        dist = abs(cord.x)+abs(cord.y)
        cost = sum([l.get_meta(cord.x,cord.y) for l in grid.layers])
        if dist < mindist: mindist = dist
        if cost < mincost: mincost = cost

print(mindist)
print(mincost)
