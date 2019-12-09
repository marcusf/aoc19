import utils
from collections import defaultdict

input = utils.read_input_multi('\n', ')', generator=str, fname='06.input')

def mk_tree(input):
    children, parents, nodes = defaultdict(list), dict(), set()
    for (parent, child) in input:
        children[parent].append(child)
        parents[child] = parent
        nodes.add(parent)
        nodes.add(child)
    return parents, children, nodes

def path_to_com(node, parents):
    output = []
    while node != 'COM':
        node = parents[node]
        output.append(node)
    return output

def distance_to_com(node, parents):
    score = 0
    while node != 'COM':
        score+=1
        node = parents[node]
    return score

def path_to_common_ancestor(node_a, node_b, parents):
    path_a = path_to_com(node_a, parents)
    path_b = path_to_com(node_b, parents)
    for i, node in enumerate(path_a):
        if node in path_b:
            partial_a = path_a[0:i+1]
            partial_b = path_b[0:path_b.index(node)+1]
            return partial_a, partial_b
    return [], []

def part_a(input):
    parents, children, nodes = mk_tree(input)
    score = 0
    for node in nodes:
        i = distance_to_com(node, parents)
        score += i
    print(score)

def part_b(input):
    parents, children, nodes = mk_tree(input)
    path_1, path_2 = path_to_common_ancestor('YOU','SAN',parents)
    print(len(path_1)-1 + len(path_2)-1)


part_a(input)
part_b(input)