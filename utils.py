import os
import sys
import numpy as np
from PIL import Image
from collections import defaultdict

def read_input(delim=',', fname='', generator=int):
    if fname == '': fname = os.path.basename(sys.argv[0]).split('.')[0] + '.input'
    if delim == None:
        return [generator(i) for i in list(open(fname,'r').read())]
    else:
        return [generator(i) for i in open(fname, 'r').read().split(delim)]

def read_input_multi(delim_1='\n', delim_2=',', fname='', generator=int):
    if fname == '': fname = os.path.basename(sys.argv[0]).split('.')[0] + '.input'
    return [([x for x in i.split(delim_2)] if delim_2 != None else list(i)) for i in open(fname, 'r').read().split(delim_1)]

# ===============================================
# An infite list representation from a finite list
class longlist(list):
    def __init__(self, lst):
        self.lst = lst
        self.last_written = 0
        self.spill = defaultdict(int)

    def __setitem__(self, index, value):            
        if index > len(self.lst)-1:
            self.last_written = index
            self.spill[index] = value
        else:
            self.lst[index] = value
        
    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.lst[index]
        elif index > len(self.lst)-1:
            return self.spill[index]
        else:
            return self.lst[index]

# ==============================================
# Basic 2D coordinates
class Coord2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self): return hash((self.x, self.y))
    def __str__(self): return f"{self.x}x{self.y}"
    def __repr__(self): return self.__str__()
    def __eq__(self, other): 
        if isinstance(other, tuple): return (self.x, self.y) == other 
        else: return (self.x, self.y) == (other.x, other.y)
    def __ne__(self, other): return not(self == other)
    def __iadd__(self, other): 
        self.x += other.x
        self.y += other.y 
        return self

    def rotate90(self):
        sx = self.x
        self.x = -self.y
        self.y = sx
    
    def rotate270(self):
        sx = self.x
        self.x = self.y
        self.y = -sx

# ===================================================
# Simple grid layer. Combine with other grid layers
# to get a grid that can compute intersections.
# Each point can have a value and a meta-value, which
# is just a place to shove shit that might be needed.
class GridLayer:

    def __init__(self, value_constructor=int, meta_constructor=int):
        self.grid = defaultdict(value_constructor)
        self.meta = defaultdict(meta_constructor)
        self.grid_bag = set()
        self.minx = sys.maxsize
        self.miny = sys.maxsize
        self.maxx = -sys.maxsize
        self.maxy = -sys.maxsize

    def __iter__(self):
        return iter(self.grid.items())

    def __getitem__(self, key):
        if isinstance(key, Coord2D):
            x, y = key.x, key.y
        else:
            x, y = key
        return self.get(x, y)

    def __setitem__(self, key, val):
        if isinstance(key, Coord2D):
            x, y = key.x, key.y
        else:
            x, y = key
        self.put(x, y, val)

    def bounds(self):
        return (self.minx, self.miny, self.maxx, self.maxy)

    def put(self, x, y, val):
        self.grid[Coord2D(x,y)] = val
        self.grid_bag.add(Coord2D(x,y))
        self.minx = min(x, self.minx)
        self.miny = min(y, self.miny)
        self.maxx = max(x, self.maxx)
        self.maxy = max(y, self.maxy)
    
    def get(self, x, y):
        return self.grid[Coord2D(x,y)]

    def put_meta(self, x, y, val):
        self.meta[Coord2D(x,y)] = val

    def get_meta(self, x, y):
        return self.meta[Coord2D(x,y)]

    def putif_meta(self, x, y, guard, val):
        if self.get_meta(x,y) == guard:
            self.put_meta(x,y,val)

    def print(self):
        minx, miny, maxx, maxy = self.bounds()
        for y in range(miny, maxy+1):
            l = []
            for x in range(minx, maxx):
                if self[(x,y)] == 1:
                    l.append('#')
                else:
                    l.append(' ')
            print(''.join(l)) 

# ========================================
# A combination of many GridLayer's
class Grid:

    def __init__(self, value_constructor=int, meta_constructor=int):
        self.layers = []
        self.value_constructor=value_constructor
        self.meta_constructor=meta_constructor

    def add_layer(self):
        layer = GridLayer(self.value_constructor, self.meta_constructor)
        self.layers.append(layer)
        return layer

    def intersection(self):
        return set.intersection(*[s.grid_bag for s in self.layers])

    def bounds(self):
        b = list(self.layers[0].bounds())
        for l in self.layers:
            nb = l.bounds()
            if nb[0] < b[0]: b[0] = nb[0]
            if nb[1] < b[1]: b[1] = nb[1]
            if nb[2] > b[2]: b[2] = nb[2]
            if nb[3] > b[3]: b[3] = nb[3]
        return tuple(b)

    # Uses numpy to output an image. Usually more helpful than text 
    # for larger grids. Varies colors.
    def pretty_image(self):
        bounds = self.bounds()
        width = bounds[2]-bounds[0]
        height = bounds[3]-bounds[1]
        off_x, off_y = -bounds[0], -bounds[1]
        print(width, height)
        array = np.full((height+1,width+1,3), 255, dtype=np.uint8)
        
        for i, l in enumerate(self.layers):
            r = 200 if (i+2) % 2 == 0 else 0
            g = 200 if (i+2) % 3 == 0 else 0
            b = 200 if (i+2) % 4 == 0 else 0
            for cord in l.grid_bag:
                array[cord.y+off_y][cord.x+off_x] = [r,g,b]
        return Image.fromarray(array).show()

