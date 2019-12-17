from utils import *
from interp import *

m = GridLayer(str)

ip = interpreter(read_input())
output, _ = ip.run_until_blocked()

# output=[ord(c) for c in '''..#..........
# ..#..........
# #######...###
# #.#...#...#.#
# #############
# ..#...#...#..
# ..#####...#..''']
# print(output)

for y, row in enumerate(''.join([chr(o) for o in output]).split("\n")):
    for x, ch in enumerate(row):
        m[(x,y)] = ch

alignments = []

for c in list(m.grid.keys()):
    item = m[c]
    if item == '#':
        if m[c+(-1,0)] == '#' and m[c+(1,0)] == '#'\
         and m[c+(0,1)] == '#' and m[c+(0,-1)] == '#':
           alignments.append((c.x,c.y))

print(sum([x*y for (x,y) in alignments]))