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
        'mode': [0,0,0],
        'eval': lambda p, args, ip, mode, inputs, rb: (rv(p, args[1], mode[0], rb)+rv(p, args[2], mode[1], rb), ip, None, None)
    },
    'mul': {
        'opcode': 2,
        'width': 4,
        'operator': '*',
        'output_arg': 3,
        'mode': [0,0,0],
        'eval': lambda p, args, ip, mode, inputs, rb: (rv(p, args[2], mode[1], rb) * rv(p, args[1], mode[0], rb), ip, None, None)
    },
    'exit': {
        'opcode': 99,
        'width': 1,
        'halt': True,
        'output_arg': -1,
        'eval': lambda p, args, ip, mode, inputs, rb: None
    },
    'ld': {
        'opcode': 3,
        'width': 2,
        'output_arg': 1,
        'mode': [0],
        'eval': lambda p, args, ip, mode, inputs, rb: (inputs.pop(0), ip, None, None)
    },
    'out': {
        'opcode': 4,
        'width': 2,
        'output_arg': 1,
        'mode': [0],
        'eval': lambda p, args, ip, mode, inputs, rb: (None, ip, p[args[1]], None)
    },
    'jnz': { # jump-if-true
        'opcode': 5,
        'width': 3,
        'output_arg': 1,
        'mode': [0,0],
        'operator': 'if 0 !=',
        'eval': lambda p, args, ip, mode, inputs, rb: (None, ip if rv(p, args[1], mode[0], rb) == 0 else rv(p, args[2], mode[1], rb), None, None)
    },
    'jz': { # jump-if-false
        'opcode': 6,
        'width': 3,
        'output_arg': 1,
        'mode': [0,0],
        'operator': 'if 0 ==',
        'eval': lambda p, args, ip, mode, inputs, rb: (None, ip if rv(p, args[1], mode[0], rb) != 0 else rv(p, args[2], mode[1], rb), None, None)
    },
    'lt': {
        'opcode': 7,
        'width': 4,
        'output_arg': 3,
        'mode': [0,0,0],
        'operator': '&lt;',
        'eval': lambda p, args, ip, mode, inputs, rb: (1 if rv(p, args[1], mode[0], rb) < rv(p, args[2], mode[1], rb) else 0, ip, None, None)
    },
    'eq': {
        'opcode': 8,
        'width': 4,
        'output_arg': 3,
        'mode': [0,0,0],
        'operator': '==',
        'eval': lambda p, args, ip, mode, inputs, rb:  (1 if rv(p, args[1], mode[0], rb) == rv(p, args[2], mode[1], rb) else 0, ip, None, None)
    },
    'rel': {
        'opcode': 9,
        'width': 2,
        'output_arg': 1,
        'mode': [0],
        'operator': 'set',
        'eval': lambda p, args, ip, mode, inputs, rb:  (None, ip, None, rv(p, args[1], mode[0], rb))

    }
}

def rv(program, arg, mode, rb):
    if mode == 0:
        return program[arg]
    elif mode == 2:
        return program[arg+rb]
    else:
        return arg

def _instr_opcode(instructions):
    opcodes = {}
    for key, val in instructions.items():
        v = val
        v['name'] = key
        opcodes[val['opcode']] = v
    return opcodes

def parse_op(i, instrs):
    op = list(str(i))
    if len(op) == 1: 
        oper = dict(instrs[i])
        return oper
    
    oper = int(''.join(op[-2:]))
    args = [int(x) for x in op[0:-2]]
    opcode = dict(instrs[oper])
    opcode['mode'] = list(reversed([0 for _ in range(opcode['width']-len(args)-1)] + args))
    return opcode

def parse(stream):
    instrs = _instr_opcode(_INSTR)
    output,mapping = [],[]
    data = stream[:]
    loc = 0
    while len(data):
        if int(str(data[0])[-2:]) in instrs:

            opcode = parse_op(data[0], instrs)
            output.append((loc, opcode,data[0:opcode['width']]))
            current_pos = len(output)-1
            mapping = mapping + [current_pos for _ in range(opcode['width'])]
            #if opcode['name'] == 'exit':
            #    return output, mapping
            data = data[opcode['width']:]
            loc += opcode['width']
        else:
            mapping = mapping + [-1]
            # Seems to be some data stuff here that we can just skip.
            loc += 1
            data = data[1:]
    return output, mapping

def print_debug(loc, op_str, opcode, args, inputs, outputs):
    in_str = f'OP = {op_str}; IP = {inputs[0]}; ARGS = ' + ', '.join([str(x) for x in inputs[1:]])
    out_str = 'IP = ' + str(outputs[0]) + '; ARGS = ' + ', '.join([str(x) for x in outputs[1:]])
    source_str = str(loc)
    name = opcode['name']
    modes = opcode['mode']
    operator = opcode['operator'] if 'operator' in opcode else ','
    if opcode['width'] == 4:
        result = f'<var>p[{args[3]}]</var>' if modes[2] == 0 else f'<dir>{args[3]}</dir>' 
        var1 = f'<var>p[{args[1]}]</var>' if modes[0] == 0 else  f'<dir>{args[1]}</dir>' 
        var2 = f'<var>p[{args[2]}]</var>' if modes[1] == 0 else  f'<dir>{args[2]}</dir>' 
        opcode_str = f'<op>{name}</op> {result} = {var1} {operator} {var2}'
    elif opcode['width'] == 2:
         opcode_str = f'<op>{name}</op> <var>p[{args[1]}]</var>'
    elif opcode['width'] == 3:
        result = f'<var>p[{args[2]}]</var>' if modes[1] == 0 else f'<dir>{args[2]}</dir>' 
        var1 = f'<var>p[{args[1]}]</var>' if modes[0] == 0 else  f'<dir>{args[1]}</dir>' 
        opcode_str = f'<op>{name}</op> {result} {operator} {var1}'
    else:
         opcode_str = f'<op>{name}</op>'

    print_formatted_text(HTML(f'<loc>{source_str}:</loc>\t{opcode_str}\t; <opt>({in_str})\t->\t({out_str})</opt>'), style=style)

def run(stream, data_input=[0], data_output=[], debug=False, printer=print_debug, tracing=False, tracing_fn=None, ip=0):
    instrs = _instr_opcode(_INSTR)
    data = stream[:]
    relative_base = 0

    while True:
        #output, mapping = parse(data)
        old_ip = ip
        op = int(str(data[ip])[-2:])
        if op in instrs:
            if op == 99: return data, data_output, ip, True # Magic breaking OP.
            if op == 3 and len(data_input) == 0:
                return data, data_output, ip, False
            op_str = data[ip]
            opcode = parse_op(op_str, instrs)
            start_ip = ip

            if opcode['output_arg'] >= 0:
                args = data[ip:(ip+opcode['width'])]
                output_arg = args[opcode['output_arg']]
                
                if debug or tracing: 
                    outp = []
                    for i, a in enumerate(args[1:]):
                        if opcode['mode'][i] == 0:
                            outp.append(data[a])
                        else:
                            outp.append(a)
                    inputs = [ip] + outp

                out_data, ip, output_data, new_rb = opcode['eval'](data, args, ip, opcode['mode'], data_input, relative_base)
                


                if out_data != None: data[output_arg] = out_data
                if output_data != None: data_output.append(output_data)
                if new_rb != None: relative_base = new_rb

                if debug or tracing: 
                    outp = []
                    for i, a in enumerate(args[1:]):
                        if opcode['mode'][i] == 0:
                            outp.append(data[a])
                        else:
                            outp.append(a)
                    outputs = [ip] + outp

                if debug: print_debug(start_ip, op_str, opcode, args, inputs, outputs)
                if tracing: tracing_fn(start_ip, opcode, args, inputs, outputs)

            if old_ip == ip:
                ip += opcode['width']
        else:
            ip += 1
    return data, data_output, ip, True

style = Style.from_dict({
    'op': 'bold',
    'var': '#aa3333',
    'dir': '#00ff00',
    'loc': '#666666',
    'opt': '#666666 italic'
})

def pretty(program):
    output = []
    for (ip, opcode, args) in program:
        output.append(str(ip) + ':\t' + opcode['pretty'].format(*args))
    return '\n'.join(output)
