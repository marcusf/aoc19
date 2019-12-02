pp = [int(i) for i in open('02.input', 'r').read().split(',')]

def run_simulator(noun, verb):
    program = pp[:]
    program[1] = noun
    program[2] = verb
    ptr = 0
    while True:
        if program[ptr] == 1:
            program[program[ptr+3]] = program[program[ptr+1]] + program[program[ptr+2]]
            ptr += 4
        elif program[ptr] == 2:
            program[program[ptr+3]] = program[program[ptr+1]] * program[program[ptr+2]]
            ptr += 4
        elif program[ptr] == 99:
            return program[0]
        else:
            return -1
    
# UPPGIFT A
print(run_simulator(12, 2))

for noun in range(0,99):
    for verb in range(99,0,-1):
        val = run_simulator(noun, verb)
        if val == 19690720:
            print(100*noun+verb)

