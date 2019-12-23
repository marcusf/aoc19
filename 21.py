from utils import *
from interp import *

def to_ascii(arr): return ''.join([chr(c) for c in arr])
def from_ascii(st): return [ord(c) for c in st]

ip = interpreter(utils.read_input())
output, _ = ip.run_until_blocked()
print(to_ascii(output))
program = open('21.program', 'r').read()
print(program)
ip.input = from_ascii(program)
output, _ = ip.run_until_blocked()
try:
    print(to_ascii(output))
except ValueError:
    print(output[-1])

# Jump if there is a hole in A or B and D is solidNOT A T
# NOT B J
# OR T J
# NOT C T
# OR T J
# NOT D T
# NOT T T
# AND T J
