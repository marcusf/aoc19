from utils import *
from interp import *
from collections import defaultdict


code = read_input()
cpus = [interpreter(code) for _ in range(50)]

for i, c in enumerate(cpus):
    c.input.append(i)
    c.run_until_blocked()

inputs = defaultdict(list)
outputs = defaultdict(list)
nat = None
naty = set()
prevy = -1

while True:
    idle = True
    for i, c in enumerate(cpus):    
        ins = inputs[i]
        #assert(len(ins) % 2 == 0)
        if len(ins) == 0:
            c.input.append(-1)
        else:
            x = ins.pop(0)
            y = ins.pop(0)
            c.input += [x,y]
            idle = False

        o, _ = c.run_until_blocked()
        if o:
            for recv, x, y in chunk(o, 3):
                if recv == 255:
                    nat = [x,y]
                #else:
                    #idle = False
                inputs[recv] += [x,y]
                #print(f'{i}: Sending ({x},{y}) to {recv}')
    if idle and nat:
        #print(f'NAT: Sending ({y}) to 0')
        if nat[1] == prevy:
            print(prevy)
        prevy = nat[1]
        inputs[0] += nat
        nat = None
