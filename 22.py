from utils import *

def compose(k1, m1, k2, m2):
    return (k1*k2, k1*m2+m1)

def reduce(lng):
    k, m = 1, 0
    for c,a in parse_input():
        if c == 0: # deal_incr_n
            kk, mm = a, 0
        elif c == 1: # deal_into_new
            kk, mm = -1, lng - 1 
        elif c == 2: # cut
            kk, mm = 1, -a
        k, m = compose(kk,mm,k,m)
    return k, m

#cmds = [deal_incr_n, deal_into_new, cut]

inp = read_input(delim='\n', generator=str)

def parse_input():
    ll = []
    for l in inp:
        if l.find('increment') >= 0: ll.append((0, int(l[l.rindex(' ')+1:])))
        elif l.find('new stack') >= 0: ll.append((1,0))
        elif l.find('cut') >= 0: ll.append((2, int(l[l.rindex(' ')+1:])))
    return ll

def part1():
    k, m = reduce(10007)
    print((k * 2019 + m) % 10007)

def part2():
    cards, iters = 119315717514047, 101741582076661
    k, m = reduce(cards)
    k %= cards
    m %= cards
    kk = pow(k, iters*(cards-2), cards)
    mm = m * pow(1-k, cards-2, cards) % cards 
    print(((2020 - mm) * kk + mm) % cards)
      

part1()
part2()