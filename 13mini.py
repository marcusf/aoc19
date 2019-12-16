from utils import *
from interp import *

score = 0

def loop(out):
    global score
    px, bx = 0, 0
    for x, y, t in chunk(out, 3):
        if x == -1 and y == 0:
            score = t
        elif t == 3:
            px = x
        elif t == 4:
            bx = x
    return [sign(bx - px)]

icp = interpreter(read_input(fname='13.input'))
icp.code[0] = 2
icp.run(loop)
print(score)