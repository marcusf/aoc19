from utils import *
from interp import *

def part1():
    c = 0
    ip = interpreter(read_input())
    for x in range(50):
        for y in range(50):
            ip.input = [x,y]
            o, _ = ip.run_until_blocked()
            if o[0] == 1:
                c+=1
            ip.restart()
    print(c)

ip = interpreter(read_input())

def check(x,y):
    global ip
    ip.restart()
    ip.input = [x,y]
    o, _ = ip.run_until_blocked()
    return o[0]

def part2():
    x, y = 1400, 0
    while True:
        o = check(x,y)
        if o == 0:
            y += 1
        else:
            if x > 99 and y > 99:
                if check(x-99,y+99) == 1:
                   print(10000*(x-99)+y)
                   return
            x += 1

part1()
part2()