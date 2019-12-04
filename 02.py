import utils
import interp

pp = utils.read_input()

def run_simulator(pp, noun, verb):
    stream = pp[:]
    stream[1] = noun
    stream[2] = verb

    program, mapping = interp.parse(stream)
    return interp.run(stream, mapping, program, debug=False)[0]
    
# UPPGIFT A
print(run_simulator(pp, 12, 2))

for noun in range(0,99):
    for verb in range(99,0,-1):
        val = run_simulator(pp, noun, verb)
        if val == 19690720:
            print(100*noun+verb)
