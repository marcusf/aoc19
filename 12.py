import utils
from utils import Coord3D
import re
import itertools
import copy 
from collections import defaultdict
import math

input = utils.read_input('\n',\
    generator=lambda s: Coord3D(*[int(i) for i in re.findall(r"([-]?\d+)", s)]))

moons = [(i, Coord3D(0,0,0)) for i in input]

def apply_gravity(p1, p2, v1, v2):
    if p1 > p2: 
        return (v1-1, v2+1)
    elif p2 > p1:
        return (v1+1, v2-1)
    else:
        return (v1,v2)

def iterate_once(ast):
    for (a1, a2) in itertools.combinations(ast, r=2):
        a1[1].x, a2[1].x = apply_gravity(a1[0].x, a2[0].x, a1[1].x, a2[1].x)
        a1[1].y, a2[1].y = apply_gravity(a1[0].y, a2[0].y, a1[1].y, a2[1].y)
        a1[1].z, a2[1].z = apply_gravity(a1[0].z, a2[0].z, a1[1].z, a2[1].z)
    for a in ast:
        a[0].x += a[1].x
        a[0].y += a[1].y
        a[0].z += a[1].z

def total_energy(a):
    pot = abs(a[0].x)+abs(a[0].y)+abs(a[0].z)
    kin = abs(a[1].x)+abs(a[1].y)+abs(a[1].z)
    return pot*kin

def find_circuits():
    coord_buckets = defaultdict(dict)
    answers = dict()
    for iter in range(3000000):
        if len(answers) == 3: break
        xs = tuple([(m[0].x, m[1].x) for m in moons])
        ys = tuple([(m[0].y, m[1].y) for m in moons])
        zs = tuple([(m[0].z, m[1].z) for m in moons])

        if xs in coord_buckets['x'] and not ('x' in answers):
            answers['x'] = (coord_buckets['x'][xs], iter)
        else:
            coord_buckets['x'][xs] = iter

        if ys in coord_buckets['y'] and not ('y' in answers):
            answers['y'] = (coord_buckets['y'][ys], iter)
        else:
            coord_buckets['y'][ys] = iter

        if zs in coord_buckets['z'] and not ('z' in answers):
            answers['z'] = (coord_buckets['z'][zs], iter)
        else:
            coord_buckets['z'][zs] = iter

        iterate_once(moons)
    return answers, coord_buckets

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

p, _ = find_circuits()
x, x_end = p['x']
y, y_end = p['y']
z, z_end = p['z']
x_cycle = x_end - x
y_cycle = y_end - y
z_cycle = z_end - z

print(x,y,z,x_cycle,y_cycle,z_cycle)
print(lcm(lcm(x_cycle,y_cycle),z_cycle))
