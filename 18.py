from utils import *

def get_map():
    start = Coord2D(0,0)
    input = read_input('\n',generator=str, fname='18.test')
    mp = GridLayer(str)
    keys, doors = dict(), dict()

    for y, row in enumerate(input):
        for x, v in enumerate(row):
            if v == '@':
                start.x = x
                start.y = y
                mp[(x,y)] = '.'
            else:
                mp[(x,y)] = v
            if v.islower():
                keys[v] = Coord2D(x,y)
            elif v.isupper():
                doors[v] = Coord2D(x,y)
    return mp, start, keys, doors

def shortest_path(grid, frm, to):
    p = frm
    winner = []
    winner_len = 999999
    queue = [(p,[])]
    while len(queue) > 0:
        point, path = queue.pop(0)
        for coord,v,_ in grid.adjacent(point):
            if coord == to:
                if len(path) < winner_len:
                    winner_len = len(path)
                    winner = path
                continue
            else:
                if v == '.' and not coord in path:
                    path.append(coord)
                    queue.append([coord,path[:]])
    return winner


def game():
    grid, start, keys, doors = get_map()
    pos = start
    total = 0
    return solve(grid, start, keys, doors, total)

def get_reachable(grid, keys, pos):
    reachables = []
    for key in list(keys.value()):
        d = shortest_path(grid, keys, pos)
        if len(d) > 0:
            reachables.append(d)
    return reachables


def solve(grid, pos, keys, doors, total):
    while len(keys) > 0:
        print(keys)
        for key in get_reachable(grid, keys, pos):
            d = shortest_path(grid,key,pos)
            total += len(d)+1

            pos = key
            key_name = grid[key]
            print(f'Unlocking {key_name.upper()}')

            if key_name.upper() in doors:
                grid[doors[key_name.upper()]] = '.'
                del doors[key_name.upper()]

            grid[pos] = '.'
            del keys[key_name]

            solve(grid, pos, keys.copy(), doors.copy(), total)


    return total        

print(game())
