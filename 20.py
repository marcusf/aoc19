from utils import *
from collections import *


def make_map():
    g = GridLayer(str)
    inner_portals = defaultdict(list)
    outer_portals = defaultdict(list)
    pcord = dict()
    mp = read_input('\n',generator=str, fname='20.input')
    y_s = 2
    y_e = -2
    x_s = mp[y_s].find('#')
    x_e = mp[y_s].rfind('#')
    for y, l in enumerate(mp[y_s:y_e]):
        for x, c in enumerate(l[x_s:x_e+1]):
            if c in ('#','.'):
                g[(x,y)] = c
            else:
                g[(x,y)] = ' '
            if c == '.':
                # CHAOS, FUCK!
                if mp[y+y_s][x+x_s-1].isalpha() and mp[y+y_s][x+x_s-2].isalpha():
                    s = mp[y+y_s][x+x_s-2]+mp[y+y_s][x+x_s-1]
                    if x >= len(l)-5 or x == 0:
                        outer_portals[s] = (x,y)
                    else:
                        inner_portals[s] = (x,y)
                    pcord[(x,y)] = s
                if mp[y+y_s][x+x_s+1].isalpha() and mp[y+y_s][x+x_s+2].isalpha():
                    s = mp[y+y_s][x+x_s+1]+mp[y+y_s][x+x_s+2]
                    if x >= len(l)-5 or x == 0:
                        outer_portals[s] = (x,y)
                    else:
                        inner_portals[s] = (x,y)
                    pcord[(x,y)] = s
                if mp[y+y_s-1][x+x_s].isalpha() and mp[y+y_s-2][x+x_s].isalpha():
                    s = mp[y+y_s-2][x+x_s]+mp[y+y_s-1][x+x_s]
                    if y < y_s or y >= len(mp)-(y_s-y_e)-1:
                        outer_portals[s] = (x,y)
                    else:
                        inner_portals[s] = (x,y)
                    pcord[(x,y)] = s
                if mp[y+y_s+1][x+x_s].isalpha() and mp[y+y_s+2][x+x_s].isalpha():
                    s = mp[y+y_s+1][x+x_s]+mp[y+y_s+2][x+x_s]
                    if y < y_s or y >= len(mp)-(y_s-y_e)-2:
                        outer_portals[s] = (x,y)
                    else:
                        inner_portals[s] = (x,y)
                    pcord[(x,y)] = s
    return g, inner_portals, outer_portals, pcord

def make_graph(g, inner_portals, inner_edges, outer_portals, outer_edges, pcord):
    edges = defaultdict(list)
    nodes = dict()
    x0,y0,x1,y1 = g.bounds()
    for x in range(x0, x1+1):
        for y in range(y0, y1+1):
            if g[(x,y)] == '.':
                nodes[(x,y)] = 0
                for p, c, _ in g.adjacent(Coord2D(x,y)):
                    if c == '.':
                        xt,yt=p
                        edges[(x,y)].append((xt,yt,0))

    for name, (xt,yt) in inner_edges.items():
        nodes[(xt,yt)] = -1
        edges[outer_edges[name]].append((xt,yt,-1))

    for name, (xt,yt) in outer_edges.items():
        nodes[(xt,yt)] = -1
        if name in inner_edges:
            edges[inner_edges[name]].append((xt,yt,1))

    return edges, nodes

def shortest_path(graph, frm, to):
    p = frm
    winner = []
    winner_len = 999999
    queue = [(p,[])]
    while len(queue) > 0:
        point, path = queue.pop(0)
        for coord in graph[point]:
            if coord == to:
                if len(path) < winner_len:
                    winner_len = len(path)
                    winner = path
                continue
            else:
                if not coord in path:
                    p = path[:]
                    p.append(coord)
                    queue.append([coord,p])
    return winner

def shortest_path_level(edges, nodes, frm, to):
    q = set([(frm[0], frm[1], 0)])
    goal = (to[0], to[1], 0)
    visited = set()
    dist = 0

    while q:
        visited.update(q)
        dist += 1
        q = {(x,y, ll+l) for xx,yy,ll in q for x,y,l in edges[(xx,yy)] if ll+l>=0} - visited
        if goal in q:
            break
    return dist

grid, inner_portals, outer_portals, pcord = make_map()

inner_coords = set(inner_portals.values())
outer_coords = set(outer_portals.values())

edges, nodes = make_graph(grid, inner_coords, inner_portals, outer_coords, outer_portals, pcord)

nodes[outer_portals['AA']] = 0
nodes[outer_portals['ZZ']] = 0

start = outer_portals['AA']
end = outer_portals['ZZ']

print(shortest_path_level(edges, nodes, outer_portals['AA'], outer_portals['ZZ']))
