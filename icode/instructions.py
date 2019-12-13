from collections import namedtuple

opcode = namedtuple('opcode', 'name, width, operator, halt, output_arg, mode, eval', defaults=(None,) * 7)

def noop(*a): return None

instructions = {
    1: opcode(name='add', width=4, operator='+', output_arg=3, mode=[0,0,0], \
         eval=lambda p, args, ip, mode, inputs, rb: (rv(p, args[1], mode[0], rb)+rv(p, args[2], mode[1], rb), ip, None, None)),
    2: opcode(name='mul', width=4, operator='*', output_arg=3, mode=[0,0,0], \
         eval=lambda p, args, ip, mode, inputs, rb: (rv(p, args[2], mode[1], rb) * rv(p, args[1], mode[0], rb), ip, None, None)),
    3: opcode(name='ld',  width=2, output_arg=1, mode=[0], \
        eval=lambda p, args, ip, mode, inputs, rb: (inputs.pop(0), ip, None, None)),
    4: opcode(name='out', width=2, output_arg=1, mode=[0], \
        eval=lambda p, args, ip, mode, inputs, rb: (None, ip, rv(p, args[1], mode[0], rb), None)),
    5: opcode(name='jnz', width=3, output_arg=1, mode=[0,0], operator='if 0 !=', \
        eval=lambda p, args, ip, mode, inputs, rb: (None, ip if rv(p, args[1], mode[0], rb) == 0 else rv(p, args[2], mode[1], rb), None, None)),
    6: opcode(name='jz',  width=3, output_arg=1, mode=[0,0], operator='if 0 ==', \
        eval=lambda p, args, ip, mode, inputs, rb: (None, ip if rv(p, args[1], mode[0], rb) != 0 else rv(p, args[2], mode[1], rb), None, None)),
    7: opcode(name='lt',  width=4, output_arg=3, mode=[0,0,0], operator='&lt;', \
        eval=lambda p, args, ip, mode, inputs, rb: (1 if rv(p, args[1], mode[0], rb) < rv(p, args[2], mode[1], rb) else 0, ip, None, None)),
    8: opcode(name='eq',  width=4, output_arg=3, mode=[0,0,0], operator='==', \
        eval=lambda p, args, ip, mode, inputs, rb:  (1 if rv(p, args[1], mode[0], rb) == rv(p, args[2], mode[1], rb) else 0, ip, None, None)),
    9: opcode(name='rel', width=2, output_arg=1, mode=[0], \
        eval=lambda p, args, ip, mode, inputs, rb:  (None, ip, None, rv(p, args[1], mode[0], rb))),
    99: opcode(name='exit', width=1, halt=True, eval=noop)
}

def rv(program, arg, mode, rb):
    if mode == 0:
        return program[arg]
    elif mode == 2:
        return program[arg+rb]
    elif mode == 1:
        return arg

def get_opcode(d):
    return int(str(d)[-2:])

def has_op(i):
    return get_opcode(i) in instructions and i > 0 and i < 99999

def parse_op(i):
    op = list(str(i))
    if len(op) == 1: return instructions[i]
    
    oper = int(''.join(op[-2:]))
    args = [int(x) for x in op[0:-2]]
    padded_args = list(reversed([0 for _ in range(instructions[oper].width-len(args)-1)] + args))
    return instructions[oper]._replace(mode=padded_args)