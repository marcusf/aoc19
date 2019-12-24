from utils import *

def deal_into_new(x,_,N): return N - 1 - x % N
def cut(x, n, N):         return x + N - n % N
def deal_incr_n(x, n, N): return x * n     % N

cmds = [deal_incr_n, deal_into_new, cut]

inp = read_input(delim='\n', generator=str)

def parse_input():
    ll = []
    for l in inp:
        if l.find('increment') >= 0: ll.append((0, int(l[l.rindex(' ')+1:])))
        elif l.find('new stack') >= 0: ll.append((1,0))
        elif l.find('cut') >= 0: ll.append((2, int(l[l.rindex(' ')+1:])))
    return ll

def apply(lng,pos):
    for c,a in parse_input():
        pos = cmds[c](pos,a,lng)
    return pos

def part1():
    lng, pos = 10007, 2019
    print(apply(lng, pos))

L, K = 119315717514047, 101741582076661

# Find x when:
# F(x)^K = 2020 => F(F(F(...F(X)...))) = 2020
# F(x)  = 2020


part1()
