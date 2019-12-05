import interp
import utils
import sys

from prompt_toolkit import prompt, print_formatted_text, HTML, prompt, PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter


style = Style.from_dict({
    'op': 'bold',
    'var': '#aa3333',
    'loc': '#666666',
    'opt': '#666666 italic'
})

def print_debug(loc, opcode, args, inputs, outputs):
    in_str = 'IP = ' + str(inputs[0]) + '; ARGS = ' + ', '.join([str(x) for x in inputs[1:]])
    out_str = 'IP = ' + str(outputs[0]) + '; ARGS = ' + ', '.join([str(x) for x in outputs[1:]])
    opcode_str = pretty_code(loc, opcode, args)
    print_formatted_text(HTML(f'{opcode_str}\t; <opt>({in_str})\t->\t({out_str})</opt>'), style=style)

def pretty_code(loc, opcode, args):
    source_str = str(loc)
    name = opcode['name']
    if opcode['width'] == 1:
        return f'<loc>{source_str}:</loc>\t<op>{name}</op>'
    else:
        operator = opcode['operator'] if 'operator' in opcode else ','
        return f'<loc>{source_str}:</loc>\t<op>{name}</op> <var>p[{args[3]}]</var> = <var>p[{args[1]}]</var> {operator} <var>p[{args[2]}]</var>'

trace_log = []

def tracer(loc, opcode, args, inputs, outputs):
    trace_log.append((loc,opcode,args,inputs,outputs))

def run(stream, debug=False, trace=False):
    program, mapping = interp.parse(stream)
    return interp.run(stream, mapping, program, debug=debug, printer=print_debug, tracing=trace, tracing_fn=tracer)[0]

stream = None
fname = None

def cli_load(args):
    global stream
    global fname
    fname = args[0]
    try:
        stream = utils.read_input(fname=fname)
        print(f'loaded {fname}')
    except:
        print(f'unable to load {fname}')

def cli_run(args):
    global stream
    verbose = 'verbose' in args
    trace = 'trace' in args
    print(f'executing {fname}, verbose={verbose}, trace={trace}')
    result = run(stream, verbose, trace)
    print(f'returned: {result}')

def cli_print(args):
    global stream
    program, _ = interp.parse(stream)
    for row in program:
        print_formatted_text(HTML(pretty_code(*row)), style=style)

def cli_poke(args):
    global stream
    pos, val = int(args[0]), int(args[1])
    stream[pos] = val
    print(f'Updating {fname}, position {pos} = {val}')

commands = {'load':  {'argc': [1],     'fn': cli_load},
            'run':   {'argc': [0,1,2], 'fn': cli_run},
            'print': {'argc': [0],     'fn': cli_print},
            'poke':  {'argc': [2],     'fn': cli_poke}}

if __name__ == '__main__':
    session = PromptSession()
    clist = list(commands.keys())
    command_completer = WordCompleter(clist)
    try:
        while True:
            text = session.prompt('> ', completer=command_completer, complete_while_typing=False)
            command = text.strip().split(' ')
            if len(command) == 0 or len(text) == 0: 
                continue
            op = command[0]
            if op in clist:
                argv = command[1:]
                if len(argv) in commands[op]['argc']:
                    commands[op]['fn'](argv)
                else:
                    argl = ', '.join([str(s) for s in commands[op]['argc']])
                    largv = len(argv)
                    print(f'expected {argl} arguments, got {largv}')
            else:
                print(f'unexpected command {command}')

    except KeyboardInterrupt:
        sys.exit(0)
            

    

