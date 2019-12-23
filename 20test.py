
with open('20.example', 'r') as f:
    r = f.read().strip('\n')

grid = [s for s in r.split('\n')]
centre = (len(grid[0]) + len(grid)*1j)/2
gc = {complex(x,y):c for y, row in enumerate(grid) for x,c in enumerate(row) if c!=' '}

# can move to adjacent '.'
# grid position: new position, level difference
edg = {p:[(np,0) for np in (p+1j**i for i in range(4)) if gc.get(np)=='.']
       for p in gc if gc.get(p) != '#'} 

portals = {}
set_portals = set()
for l1 in gc:  # candidate portal label
    if gc[l1] in '.# ':  # not in a label
        continue
    # Locate portals by their label that is only adjacent to 1 other label character
    adj = gc.keys() & {l1+1j**i for i in range(4)}
    if len(adj)==1:
        l2 = adj.pop()
        pp = (l2-l1)*2 + l1  # the actual . position
        assert gc[pp]=='.'
        name = ''.join(sorted(gc[l1]+gc[l2]))  # canonical name
        if name in portals:
            pa = pp
            pb = portals[name]
            if abs(pp-centre)<abs(l1-centre):  # label of pa is further out than pa: outside
                # print(f"adding portal {name} from {pa} (outside) to {pb} (inside)")
                edg[pa].append((pb, -1))  # going from outside in: level decrease
                edg[pb].append((pa, 1))
            else:
                # print(f"adding portal {name} from {pb} (outside) to {pa} (inside)")
                edg[pa].append((pb, 1))
                edg[pb].append((pa, -1))
            set_portals.add(name)
        else:
            portals[name] = pp

# print(portals.keys() - set_portals)  # debug - unconnected portals

# BFS
def main(part):
    start = (portals['AA'], 0)
    goal = (portals['ZZ'], 0)
    visited = set()
    q = {start}
    dist=0
    while q:
        # visit
        visited.update(q)
        # expand
        q = {(np, cd+dd) for p,cd in q for np,dd in edg[p]
             if part==1 or cd+dd>=0} - visited
        # part 2 requirement is level>=0
        dist+=1
        if part==1:
            if any(p==goal[0] for p,lvl in q):
                break
        if part==2:
            if goal in q:
                break
    print(f"Part {part}: {dist}")


edg = {k: v for k,v in edg.items() if len(v) > 0}
#print(len(edg.keys()))

#print(portals)

l = {(round(k.real)-2,round(k.imag)-2): [(round(p.real)-2,round(p.imag)-2,q) for p, q in v] for k,v in edg.items() if len(v) > 0}
for k in sorted(l.keys()):
    print(k, l[k])
#main(1)
#main(2)

