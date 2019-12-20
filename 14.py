import utils
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

def parse(str):
    result = []
    for s in str.split(', '):
        v = s.split(' ')
        result.append((int(v[0]), v[1]))
    return result

data = utils.read_input_multi(delim_2=' => ', fname='14.input')
data = dict([(parse(out)[0][1], (parse(out)[0][0], parse(inn))) for (inn, out) in data])

def tryfuel(fuel, outs):
    need = defaultdict(int)
    need['FUEL'] = fuel
    have = defaultdict(int)
    
    while True:
        try:
            ingredient = next(n for n in need if n != 'ORE')
        except StopIteration:
            break

        amount, inputs = outs[ingredient]
        
        units = need[ingredient] // amount
        remainder = need[ingredient] % amount
        del need[ingredient]

        if remainder != 0:
            have[ingredient] = amount - remainder
            units += 1

        for amt2, ingred2 in inputs:
            need[ingred2] += units * amt2 - have[ingred2]
            del have[ingred2]

    return need['ORE']

print(tryfuel(1, data))

print(1000000000000)
print(tryfuel(1670299, data))