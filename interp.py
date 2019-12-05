# Assume:
# A program is a list of integers that represent some type of intcode
# of the shape:
# INSTR arg0 arg1 ...
# Where each INSTR has an INSTR_WIDTH that gives the total width of that
# instruction (minimally 1).
# So if INSTR 0 = MUL, WIDTH 3, then [0,1,5] = MUL 1 5
from prompt_toolkit import prompt, print_formatted_text, HTML
from prompt_toolkit.styles import Style

_INSTR = {
    'add': {
        'opcode': 1,
        'width': 4,
        'operator': '+',
        'output_arg': 3,
        'eval': lambda program, args, ip: (program[args[2]] + program[args[1]], ip)
    },
    'mul': {
        'opcode': 2,
        'width': 4,
        'operator': '*',
        'output_arg': 3,
        'eval': lambda program, args, ip: (program[args[2]] * program[args[1]], ip)
    },
    'exit': {
        'opcode': 99,
        'width': 1,
        'halt': True,
        'output_arg': -1,
        'eval': lambda program, args, ip: None
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
        current_pos = len(output)-1
        mapping = mapping + [current_pos for _ in range(opcode['width'])]
        if op == 99:
            return output, mapping
        data = data[opcode['width']:]
        ip += opcode['width']

def print_debug(loc, opcode, args, inputs, outputs):
    in_str = 'IP = ' + str(inputs[0]) + '; ARGS = ' + ', '.join([str(x) for x in inputs[1:]])
    out_str = 'IP = ' + str(outputs[0]) + '; ARGS = ' + ', '.join([str(x) for x in outputs[1:]])
    source_str = str(loc)
    name = opcode['name']
    operator = opcode['operator'] if 'operator' in opcode else ','
    opcode_str = f'<op>{name}</op> <var>p[{args[3]}]</var> = <var>p[{args[1]}]</var> {operator} <var>p[{args[2]}]</var>'
    print_formatted_text(HTML(f'<loc>{source_str}:</loc>\t{opcode_str}\t; <opt>({in_str})\t->\t({out_str})</opt>'), style=style)

def run(stream, mapping, output, debug=False, printer=print_debug, tracing=False, tracing_fn=None):
    instrs = _instr_opcode(_INSTR)
    data = stream[:]
    ip = 0
    while True:
        op = data[ip]
        if not op in instrs: exit(f'{op} not recognized, bailing.')
        if op == 99: return data # Magic breaking OP.
        source, opcode, _ = output[mapping[ip]]
        if opcode['output_arg'] >= 0:
            args = data[ip:(ip+opcode['width'])]
            output_arg = args[opcode['output_arg']]
            
            if debug or tracing: inputs = [ip] + [data[a] for a in args[1:]]

            data[output_arg], ip = opcode['eval'](data, args, ip)

            if debug or tracing: 
                outputs  = [ip] + [data[a] for a in args[1:]]
                
            if debug:
                print_debug(source, opcode, args, inputs, outputs)

            if tracing:
                tracing_fn(source, opcode, args, inputs, outputs)

        ip += opcode['width']
    return data

style = Style.from_dict({
    'op': 'bold',
    'var': '#aa3333',
    'loc': '#666666',
    'opt': '#666666 italic'
})

def pretty(program):
    output = []
    for (ip, opcode, args) in program:
        output.append(str(ip) + ':\t' + opcode['pretty'].format(*args))
    return '\n'.join(output)
