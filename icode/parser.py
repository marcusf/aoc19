from prompt_toolkit import print_formatted_text, HTML
from icode.instructions import parse_op, has_op, get_opcode
from icode.debug import print_debug, pretty_code, style

def parse(stream):
    output,mapping = [],[]
    data = stream[:]
    loc = 0
    while len(data):
        if has_op(data[0]):
            opcode = parse_op(data[0])
            output.append((loc, opcode,data[0:opcode.width]))
            current_pos = len(output)-1
            mapping = mapping + [current_pos for _ in range(opcode.width)]
            data = data[opcode.width:]
            loc += opcode.width
        else:
            mapping = mapping + [-1]
            loc += 1
            data = data[1:]
    return output, mapping

def print_parsed(stream):
    program, _ = parse(stream)
    for row in program:
        print_formatted_text(HTML(pretty_code(*row)), style=style)
