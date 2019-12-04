from math import floor
import utils

input = utils.read_input('\n')

def fuel(n): return floor(n/3)-2

# A
print(sum([fuel(n) for n in input]))

# B
total=0
for row in input:
    remaining = row
    while remaining > 0:
        remaining = fuel(remaining)
        total += max(0, remaining)

print(total)
