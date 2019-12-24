from utils import *

SIZE = 5

def mk_map():
    i = 0
    f = read_input_multi(delim_2=None)
    for y, row in enumerate(f):
        for x, c in enumerate(row):
            if c == '#':
                i |= 1 << (SIZE*y+x)
    return i

def pretty(mp):
    c = []
    for y in range(SIZE):
        c.append(''.join(['#' if has_bug(mp,x,y) else '.' for x in range(SIZE)]))
    return '\n'.join(c)
            

def adjacent(x,y):
    return [(x,y) for x,y in [(x+1,y),(x-1,y),(x,y-1),(x,y+1)] if x >= 0 and x < SIZE and y >=0 and y < SIZE]

def has_bug(mp,x,y):
    return (mp & 1 << SIZE*y+x) > 0

def infest(mp,x,y):
    return mp | 1 << (SIZE*y+x)

def die(mp,x,y):
    return mp & ~(1 << (SIZE*y+x))

def count_bugs(mp): 
    count = 0
    while (mp): 
        mp &= (mp-1)  
        count+= 1
    return count

def iterate1(mp):
    mm = mp
    for i in range(SIZE*SIZE):
        y, x = divmod(i, SIZE)        
        ll = len([1 for xx,yy in adjacent(x,y) if has_bug(mp,xx,yy)]) 
        if has_bug(mp,x,y) and ll != 1:
            mm = die(mm,x,y)
        elif not has_bug(mp,x,y) and ll >= 1 and ll <= 2:
            mm = infest(mm,x,y)
    return mm

def recursive_adjacents(i,lvl):
    y, x = divmod(i, SIZE)
    adjacents = [(lvl,p) for p in adjacent(x,y) if p != (2,2)]
    if i == 7:
        adjacents += [(lvl+1,(i,0)) for i in range(SIZE)]
    if i == 11:
        adjacents += [(lvl+1,(0,i)) for i in range(SIZE)]
    if i == 13:
        adjacents += [(lvl+1,(SIZE-1,i)) for i in range(SIZE)]
    if i == 17:
        adjacents += [(lvl+1,(i,SIZE-1)) for i in range(SIZE)]
    if y == 0: # TOP ROW
        adjacents += [(lvl-1,(2,1))]
    if x == 0:
        adjacents += [(lvl-1,(1,2))]
    if y == SIZE-1:
        adjacents += [(lvl-1,(2,3))]
    if x == SIZE-1:
        adjacents += [(lvl-1,(3,2))]
    return adjacents


def iterate2(mps):
    mms = mps[:]
    for lvl, mp in enumerate(mps):
        for i in range(SIZE*SIZE):
            if i == 12: 
                continue
            y, x = divmod(i, SIZE)
            adjacents = recursive_adjacents(i, lvl)
            ll = len([1 for l,(xx,yy) in adjacents if has_bug(mps[l] if l >=0 and l < len(mps) else 0,xx,yy)]) 
            if has_bug(mp,x,y) and ll != 1:
                mms[lvl] = die(mms[lvl],x,y)
            elif not has_bug(mp,x,y) and ll >= 1 and ll <= 2:
                mms[lvl] = infest(mms[lvl],x,y)
    return mms

def part1():
    mp = mk_map()
    visited = set()
    while True:
        visited.add(mp)
        mp = iterate1(mp)
        if mp in visited:
            print(mp)
            break

def part2():
    maps = [0 for _ in range(1000)]
    maps[len(maps)//2] = mk_map()
    for _ in range(200):
        maps = iterate2(maps)
    print(sum([count_bugs(m) for m in maps]))

part1()
part2()
