from utils import *
from interp import *
from itertools import *

sequence = []
navi = []
inps = []

ip = interpreter(read_input())
inps = ['west', 'take hologram', 'north', 'take space heater', 'south', 'south', 'north', 'east', 'north', 
        'south', 'east', 'take festive hat', 'east', 'take food ration', 'east', 'take spool of cat6', 'west', 
        'north', 'south', 'east', 'west', 'east', 'west', 'west', 'west', 'north', 'south', 'west', 'north', 'east', 'take space law space brochure', 
        'south', 'north', 'west', 'south', 'east', 'east', 'south', 'east', 'east', 'east', 'south', 'inv']

while inps:
    rv = inps.pop(0)
    ip.input = [ord(o) for o in rv+'\n']
    o, _ = ip.run_until_blocked()

s = (''.join([chr(c) for c in o])).split('\n')
inventory = []

for item in s:
    if len(item) > 0 and item[0] == '-':
        inventory.append(item[2:])

end = False
for i in range(2,len(inventory)):
    if end:
        break
    attempts = list(combinations(inventory,i))
    for attempt in attempts:
        start = [f'drop {i}\n' for i in inventory]
        then = [f'take {i}\n' for i in attempt]
        moves = start + then + ['south\n']
        for m in moves:
            ip.input = [ord(o) for o in m+'\n']
            o, _ = ip.run_until_blocked()
        s = ''.join([chr(c) for c in o])
        if 'Analysis complete!' in s:
            print(s[s.index('typing ')+len('typing '):s.index(' on the key')])
            end = True
            break
