from itertools import cycle, accumulate
from utils import read_input


def mull(num, n):
    pat = [0,1,0,-1]
    s = 0
    for i, v in enumerate(num):
        idx = ((i+1)//n)%4 
        s = s + v * (pat[idx])
    v = abs(s)
    return v - v//10*10

def transform(nums):
    return [mull(nums, n+1) for n, _ in enumerate(nums)]

def fft(num):
    for i in range(100):
        num = transform(num)
    return num


def part1():
    num=read_input(delim=None)
    print("".join(str(i) for i in fft(num)[:8]))

# Had to get some help... realised the matrix started looking like
# 0000 1111 at bottom half, but didn't make the leap on input.
def part2():
    num=read_input(delim=None)
    offset = int(''.join(str(s) for s in num[:7]))
    list_start = 10000 * len(num) - offset
    # Start backwards
    i = cycle(reversed(num))
    arr = [next(i) for _ in range(list_start)]
    for _ in range(100):
        arr = [n % 10 for n in accumulate(arr)]
    print("".join(str(i) for i in arr[-1:-9:-1]))

part1()
part2()