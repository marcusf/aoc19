import interp
from interp import interpreter
import utils
from utils import Coord2D
from os import system
from time import sleep

def draw(i):
    if i == 0: return ' ' #0 is an empty tile. No game object appears in this tile.
    if i == 1: return '#' #1 is a wall tile. Walls are indestructible barriers.
    if i == 2: return 'x' #2 is a block tile. Blocks can be broken by the ball.
    if i == 3: return '-' #3 is a horizontal paddle tile. The paddle is indestructible.
    if i == 4: return 'o' #4 is a ball tile. The ball moves diagonally and bounces off objects.
    return '?'

def game_loop(input, surface):
    sleep(0.01)
    system('clear')
    score = -1
    for x,y,tile in utils.chunk(input, 3):
        if x == -1 and y == 0:
            score = tile
        else:
            surface[(x,y)] = tile
        if tile == 3:
            paddle_x = x
        if tile == 4:
            ball_x = x
    surface.print(factory=draw)
    if score > -1: print("SCORE: ", score)
    return [utils.sign(ball_x - paddle_x)]

def run():
    code = utils.read_input()    
    surface = utils.GridLayer(int)
    code[0] = 2 # Put it in free mode
    icp = interpreter(code)
    icp.input.append(0)
    icp.run(input_provider=game_loop, surface=surface)

run()
