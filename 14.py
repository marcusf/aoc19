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

data = utils.read_input_multi(delim_2=' => ', fname='14.example')
data = [(parse(out)[0], parse(inn)) for (inn, out) in data]

graph = nx.DiGraph()
for node, edges in data:
    m, v = node
    graph.add_node(v,mul=m)
    for c, e in edges:
        graph.add_edge(e,v,cost=c)

print(list(nx.topological_sort(graph)))

recipe = dict()
minunits = dict()

for out, inn in data:
    recipe[out[1]] = dict([(b,a) for (a,b) in inn])
    minunits[out[1]] = out[0]

def ask_for(ingredient, amount):
    multiple = minunits[ingredient]
    n = 0
    while n < amount: n += multiple
    return n

# Convert (C, 5, ORE) = 7 
def convert(in_in, out_in, amount):
    conversion_rate = recipe[in_in][out_in]
    min_ask = ask_for(in_in, amount) // minunits[in_in]
    return conversion_rate * min_ask


def produce(in_in, amount):
    if in_in in recipe:
        return [(ing, convert(in_in, ing, amount)) for ing in recipe[in_in]]
    else:
        return []

costs = defaultdict(int)

def resolve(node, cost, costs):
    nodes = produce(node, cost)
    for node, cost in nodes:
        if node == 'ORE':
            continue
        costs[node] += cost
        stack = [(node, cost)]
        while len(stack) > 0:
            n, c = stack.pop()
            outs = produce(n, c)
            for nn, cc in outs:
                if nn == node:
                    costs[node] += cc
                stack.append((nn,cc))
        resolve(node, cost, costs)

resolve('FUEL', 1, costs)
adjacent_ore = []
for a, b in data:
    if len(b) == 1 and b[0][1] == 'ORE':
        adjacent_ore.append(a[1])
print(costs)
cost = 0
for o in adjacent_ore:
    cost += convert(o, 'ORE', costs[o])
print(cost)

# def produce_recursed(in_in, amount):
#     asks = dict(produce(in_in, amount))
#     costs = defaultdict(int)
#     for ing, amt in asks.items():
#         vals = dict(produce(ing, amt))
#         for k, v in vals.items():
#             costs[k] += v
#     print(costs)
#     return costs

# ingreds = produce_recursed('FUEL', 1)
# costs = defaultdict(int)
# for k, v in ingreds.items():
#     if k in recipe:
#         ks = produce(k,v)
#         for kk, vv in ks:
#             costs[kk] += vv

# print(costs)