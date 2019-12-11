import utils
from collections import defaultdict, namedtuple
from math import floor, ceil, copysign, gcd, atan2, pi, degrees, hypot

mp = utils.read_input_multi(delim_2=None, fname='10.input', generator=str)
point = namedtuple('Point','x,y')

coords = []
width = len(mp[0])
height = len(mp)

for y, row in enumerate(mp):
    for x, coord in enumerate(row):
        if coord == '#':
            coords.append(point(x=x,y=y))

def part1():
    distincts = defaultdict(set)
    removed = set()
    for p in coords:
        angles = set()
        for test in coords:
            d = point(x=test.x-p.x, y=test.y-p.y)
            if d.x == 0:
                angles.add(point(0,-round(copysign(1,y))))
                angles.add(point(0,round(copysign(1,y))))
            elif d.y == 0:
                angles.add(point(round(copysign(1,x)),0))
                angles.add(point(-round(copysign(1,x)),0))
            else:
                g = gcd(abs(d.x), abs(d.y))
                d = point(x=d.x//g, y=d.y//g)
                angles.add(d)
        for d in angles:
            i = 0
            pp = point(x=round(p.x+i*d.x), y=round(p.y+i*d.y))
            while pp.x >= 0 and pp.x < width and pp.y >= 0 and pp.y < 100:
                pp = point(x=round(p.x+i*d.x), y=round(p.y+i*d.y))
                if pp in coords and pp != p:
                    distincts[p].add(pp)
                    removed.add(pp)
                    break
                i += 1

    maxv, maxp, maxl = 0,(0,0),[]
    for k,v in distincts.items():
        if len(v) >= maxv:
            maxp = k
            maxv = len(v)
            maxl = v
    print(maxp, maxv)
    return removed, maxp, maxl

_, center, nuked = part1()
relcoords = [(n.x-center.x, n.y-center.y) for n in nuked if not (n.x==center.x and n.y==center.y)]

#quad1 = [p for p in relcoords if p[0] >= 0 and p[1] <= 0]
#print(sorted(quad1, key=lambda r: atan2(r[1],r[0])))


test = sorted(relcoords, key=lambda r: (atan2(r[1],r[0])))
##tt = [(ceil(-90+degrees(atan2(y,x))), x, y) for (x,y) in test]
start = test.index((0,-1))

t2 = test[start:] + test[:start]
#print(len(test))
remade = [(t[0]+center.x, t[1]+center.y) for t in t2]
print(remade[199][0]*100+remade[199][1])
#print(t2[199][1]+center.x, t2[199][2]+center.y)
