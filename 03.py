from collections import defaultdict
pp = [[x for x in i.split(",")] for i in open('03.input', 'r').read().split("\n")]
    
grid, costs = defaultdict(int), [defaultdict(int),defaultdict(int)]

def encode(x,y): return f"{x}x{y}"

def parse_one(grid, costs, current_pos, instr, wire, cost):
    x, y = current_pos
    dist = int(instr[1:])
    if instr[0] == 'R': 
        for dx in range(0,dist): 
            grid[encode(x+dx,y)] += wire
            if costs[encode(x+dx,y)] == 0:
                costs[encode(x+dx,y)] = cost+dx
        return (x+dist, y), cost+dist
    elif instr[0] == 'L': 
        for dx in range(0,dist): 
            grid[encode(x-dx,y)] += wire
            if costs[encode(x-dx,y)] == 0:
                costs[encode(x-dx,y)] = cost+dx
        return (x-dist, y), cost+dist
    elif instr[0] == 'U': 
        for dy in range(0,dist): 
            grid[encode(x,y+dy)] += wire
            if costs[encode(x,y+dy)] == 0:
                costs[encode(x,y+dy)] = cost+dy
        return (x, y+dist), cost+dist
    elif instr[0] == 'D': 
        for dy in range(0,dist): 
            grid[encode(x,y-dy)] += wire
            if costs[encode(x,y-dy)] == 0:
                costs[encode(x,y-dy)] = cost+dy
        return (x, y-dist), cost+dist
    else:
        print("Error")
        exit()

primes = [3,5]

for i, line in enumerate(pp):
    pos = (0,0)
    cost = 0
    for item in line:
        pos, cost = parse_one(grid, costs[i], pos, item, primes[i], cost)

mindist, mincost = 9999999999999, 9999999999999

for coord, its in grid.items():
    if its == 8 and coord != '0x0':
        x, y = [int(x) for x in coord.split('x')]
        dist = abs(x)+abs(y)
        if dist < mindist:
            mindist = dist
        cost = costs[0][coord] + costs[1][coord]
        if cost < mincost:
            mincost = cost

print(mindist)
print(mincost)
#print(costs)