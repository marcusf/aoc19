# Assume:
# A program is a list of integers that represent some type of intcode
# of the shape:
# INSTR arg0 arg1 ...
# Where each INSTR has an INSTR_WIDTH that gives the total width of that
# instruction (minimally 1).
# So if INSTR 0 = MUL, WIDTH 3, then [0,1,5] = MUL 1 5

_INSTR = {
    'ADD': {
        'opcode': 1,
        'width': 4,
        'pretty': 'ADD p[{3}]\t=\tp[{1}]\t+\tp[{2}]',
        'output_arg': 3,
        'eval': lambda program, args: program[args[2]] + program[args[1]]
    },
    'MUL': {
        'opcode': 2,
        'width': 4,
        'pretty': 'MUL p[{3}]\t=\tp[{1}]\t*\tp[{2}]',
        'output_arg': 3,
        'eval': lambda program, args: program[args[2]] * program[args[1]]
    },
    'EXIT': {
        'opcode': 99,
        'width': 1,
        'halt': True,
        'pretty': 'EXIT',
        'output_arg': -1,
        'eval': lambda program, args: None
    }
}

def _instr_opcode(instructions):
    opcodes = {}
    for key, val in instructions.items():
        v = val
        v['name'] = key
        opcodes[val['opcode']] = v
    return opcodes


def parse(stream):
    instrs = _instr_opcode(_INSTR)
    output,mapping = [],[]
    data = stream[:]
    ip = 0
    while len(data):
        op = data[0]
        if not op in instrs: exit(f'{op} not recognized, bailing.')
        opcode = instrs[op]
        output.append((ip, opcode,data[0:opcode['width']]))
        just_added = len(output)-1
        mapping = mapping + [just_added for _ in range(opcode['width'])]
        if 'halt' in opcode and opcode['halt']:
            return output, mapping
        data = data[opcode['width']:]
        ip += opcode['width']
        

def run(stream, mapping, output, debug=False):
    instrs = _instr_opcode(_INSTR)
    data = stream[:]
    ip = 0
    while True:
        op = data[ip]
        if not op in instrs: exit(f'{op} not recognized, bailing.')
        if op == 99: return data
        source, opcode, _ = output[mapping[ip]]
        if opcode['output_arg'] >= 0:
            args = data[ip:(ip+opcode['width'])]
            output_arg = args[opcode['output_arg']]
            exec_input = ', '.join([str(data[a]) for a in args[1:]])
            data[output_arg] = opcode['eval'](data, args)
            exec_result  = ', '.join([str(data[a]) for a in args[1:]])
            condensed = ','.join([str(a) for a in args[1:]])
            if debug:
                print(str(source) + ':\t' + opcode['pretty'].format(*args) + f'\t; [{condensed}]:\t({exec_input})\t->\t({exec_result})')
        ip += opcode['width']
    return data

def pretty(program):
    output = []
    for (ip, opcode, args) in program:
        output.append(str(ip) + ':\t' + opcode['pretty'].format(*args))
    return '\n'.join(output)
