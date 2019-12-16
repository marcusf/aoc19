from prompt_toolkit import prompt, print_formatted_text, HTML
from prompt_toolkit.styles import Style

def print_debug(loc, op_str, opcode, args, inputs, outputs, rel_base, new_rel_base):
    in_str = f'OP = {op_str}; IP = {inputs[0]}; RB={rel_base}; ARGS = ' + ', '.join(inputs[1:])
    out_str = f'IP = {outputs[0]};  RB={new_rel_base}; ARGS = ' + ', '.join(outputs[1:])
    opcode_str = pretty_code(loc, opcode, args, rel_base)
    print_formatted_text(HTML(f'{opcode_str}\t; <opt>({in_str})\t->\t({out_str})</opt>'), style=style)

def var_arg(arg, mode, rel_base):
    op = '' if arg < 0 else '+'
    return f'<var>p[{arg}]</var>' if mode == 0 else \
        f'<dir>{arg}</dir>'       if mode == 1 else \
        (f'<rvar>p[{rel_base+arg}]</rvar>' if isinstance(rel_base, int) else f'<rvar>p[{rel_base}{op}{arg}]</rvar>')

def fmt_args(args, modes, rel_base):
    return [var_arg(arg, mode, rel_base) for arg, mode in zip(args[1:], modes)]

__opcode_table = {
    1: '<op>{name}</op>',
    2: '<op>{name}</op> {vars[0]}',
    3: '<op>{name}</op> {vars[1]} {operator} {vars[0]}',
    4: '<op>{name}</op> {vars[2]} = {vars[0]} {operator} {vars[1]}'
}

def pretty_dummy(loc, name, modes, width, args, operator=',', rel_base='base'):
    vars = fmt_args(args, modes, rel_base)
    return f'<loc>{loc}:</loc>\t{__opcode_table[width].format(name=name,operator=operator,vars=vars)}\t'
()
def pretty_code(loc, opcode, args, rel_base='base'):
    #source_str = str(loc)
    name, modes, width = opcode.name, opcode.mode, opcode.width
    operator = opcode.operator if opcode.operator != None else ','
    vars = fmt_args(args, modes, rel_base)
    return f'<loc>{loc}:</loc>\t{__opcode_table[width].format(name=name,operator=operator,vars=vars)}\t'

def pretty_args(stream, ip, args, opcode, relative_base):
    outp = []
    for i, a in enumerate(args[1:]):
        if opcode.mode[i] == 0:
            outp.append(f'DIR: {a}->{stream[a]}')
        elif opcode.mode[i] == 2: 
            outp.append(f'REL: {a},{relative_base+a}->{stream[relative_base+a]}')
        else:
            outp.append(f'CONST: {a}')
    return [ip] + outp

style = Style.from_dict({
    'op': 'bold',
    'var': '#aa3333',
    'dir': '#00ff00',
    'loc': '#666666',
    'opt': '#666666 italic',
    'rvar': '#aa55ff'
})
