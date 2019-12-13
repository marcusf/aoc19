import interp
import utils
from utils import Coord2D
from os import system
from time import sleep

#0 is an empty tile. No game object appears in this tile.
#1 is a wall tile. Walls are indestructible barriers.
#2 is a block tile. Blocks can be broken by the ball.
#3 is a horizontal paddle tile. The paddle is indestructible.
#4 is a ball tile. The ball moves diagonally and bounces off objects.

def draw(i):
    if i == 0: return ' '
    if i == 1: return '#'
    if i == 2: return 'x'
    if i == 3: return '-'
    if i == 4: return 'o'
    return '?'

def run():
    code = utils.read_input()    
    finished = False
    ip, rb = 0, 0
    surface = utils.GridLayer(int)
    controller = [0]

    code[0] = 2 # Put it in free mode

    while not finished:
        sleep(0.01)
        system('clear')
        score, paddle_x, ball_x = -1, 0, 0
        code, output, ip, rb, finished = interp.run(code, data_input=controller,\
            data_output=[], verbose=False, ip=ip, relative_base=rb)
            
        for x,y,tile in utils.chunk(output, 3):
            if x == -1 and y == 0:
                score = tile
            else:
                surface[(x,y)] = tile
            if tile == 3:
                paddle_x = x
            if tile == 4:
                ball_x = x


        surface.print(factory=draw)
        controller.append(utils.sign(ball_x - paddle_x))

        if score > -1:
            print("SCORE: ", score)

    return output

run()
