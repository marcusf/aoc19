import utils, interp, itertools

stream = utils.read_input()

def run_gen(stream, phase, input, ip=0):
    code, b, ip, finished = interp.run(stream, data_input=[phase,input], data_output=[], debug=False, ip=ip)
    return b[0], code, ip, finished

def run_gen_s(stream, input, ip=0):
    code, b, ip, finished = interp.run(stream, data_input=[input], data_output=[], debug=False, ip=ip)
    return b[0] if len(b) > 0 else 0, code, ip, finished

def thrusters(stream, phases):
    input = 0
    for p in phases:
        input, code, ip, finished = run_gen(stream, p, input)
    return input, code, ip, finished

def part_1():
    max_p = 0
    max_t = []

    for s in itertools.permutations(range(5),5):
        o, _, _, _ = thrusters(stream, s)
        if o > max_p:
            max_p = o
            max_t = s

    print(f'Sequence {max_t} generated thrust {max_p}')

def feedback_thrust(stream, phases):
    engines = [(phases[i], stream[:], 0, False) for i in range(5)]

    # Warm them up. 
    for i in range(5):
        engines[i] = run_gen_s(engines[i][1], phases[i], engines[i][2])

    # Start the feedback engine
    while all([not e[3] for e in engines]):
        for i in range(5):
            input = engines[i-1][0] if i >= 1 else engines[4][0]
            #print(f'E{i} with input={input}, ip={engines[i][2]}, phase={phases[i]}')
            engines[i] = run_gen_s(engines[i][1], input, engines[i][2])
    
    return engines[4][0]


def part_2():
    stream = utils.read_input(fname='07.input')
    
    max_p = 0
    max_t = []

    for s in itertools.permutations(range(5,10),5):
        o = feedback_thrust(stream, s)
        if o > max_p:
            max_p = o
            max_t = s

    print(f'Sequence {max_t} generated thrust {max_p}')


part_1()
part_2()