import interp
import utils

def run(start):
    code = utils.read_input()    
    finished = False
    ip, rb = 0, 0
    surface = utils.GridLayer()
    direction = utils.Coord2D(0,-1) 
    pos = utils.Coord2D(0,0)
    has_hit = set()
    surface[(0,0)] = start

    while not finished:
        code, output, ip, rb, finished = interp.run(code, data_input=[surface[pos]], data_output=[], verbose=False, ip=ip, relative_base=rb)
        color, turn = output
        surface[pos] = color
        has_hit.add((pos.x,pos.y))
        if turn == 0:
            direction.rotate270()
        elif turn == 1:
            direction.rotate90()
        pos += direction

    print(len(has_hit))
    return surface

surface = run(1)
surface.print()
